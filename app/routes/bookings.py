from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import User, Booking, PhotographerAvailability
from datetime import datetime
from app.utils.decorators import login_required

bookings_bp = Blueprint('bookings', __name__)

@bookings_bp.route('/book', methods=['GET', 'POST'])
def book():
    if 'user_id' not in session:
        flash('Please log in to book a photographer.')
        return redirect(url_for('main.login'))
    
    if request.method == 'POST':
        photographer_id = request.form.get('photographer_id')
        slot_id = request.form.get('slot_id')
        name = request.form.get('name')
        email = request.form.get('email')
        notes = request.form.get('notes')
        
        if not photographer_id or not slot_id:
            flash('Please select a photographer and time slot.')
            return redirect(url_for('bookings.book'))
        
        # Get the availability slot
        slot = PhotographerAvailability.query.get(slot_id)
        if not slot or slot.photographer_id != int(photographer_id):
            flash('Invalid time slot selected.')
            return redirect(url_for('bookings.book'))
        
        # Check if slot is still available
        if not slot.is_available:
            flash('This time slot is no longer available.')
            return redirect(url_for('bookings.book'))
        
        # Combine date and time
        booking_datetime = datetime.combine(
            slot.available_date, 
            datetime.strptime(slot.start_time, '%H:%M').time()
        )
        
        # Create booking
        new_booking = Booking(
            client_id=session['user_id'],
            photographer_id=int(photographer_id),
            booking_date_and_time=booking_datetime,
            type='session',
            description=notes
        )
        db.session.add(new_booking)
        
        # Mark slot as unavailable
        slot.is_available = False
        
        db.session.commit()
        
        # Redirect to confirmation page
        return redirect(url_for('bookings.booking_confirmation', booking_id=new_booking.id))
    
    # GET request - show form
    # Get all users with photographer role
    photographers = User.query.filter_by(role='photographer').all()
    photographer_map = {p.id: {'name': p.name, 'id': p.id} for p in photographers}
    
    return render_template('book.html', photographers=photographer_map)

@bookings_bp.route('/booking-confirmation/<booking_id>')
def booking_confirmation(booking_id):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    booking = Booking.query.get(booking_id)
    if not booking or booking.client_id != session['user_id']:
        flash('Booking not found.')
        return redirect(url_for('main.index'))
    
    # Get photographer name from User table
    photographer = User.query.get(booking.photographer_id)
    photographer_name = photographer.name if photographer else 'Unknown'
    
    return render_template('booking_confirmation.html', 
                         booking=booking,
                         photographer_name=photographer_name)

@bookings_bp.route('/bookings')
def bookings():
    if 'user_id' not in session:
        flash('Please log in to view bookings.')
        return redirect(url_for('main.login'))
    
    user = User.query.get(session['user_id'])
    
    # If user is a photographer, show their bookings
    if user.role == 'photographer':
        user_bookings = Booking.query.filter_by(photographer_id=user.id).order_by(Booking.booking_date_and_time.desc()).all()
    # If user is a client, show their bookings
    else:
        user_bookings = Booking.query.filter_by(client_id=user.id).order_by(Booking.booking_date_and_time.desc()).all()
    
    return render_template('bookings.html', bookings=user_bookings, user=user)


@bookings_bp.route('/bookings/<booking_id>')
def booking_detail(booking_id):
    if 'user_id' not in session:
        flash('Please log in to view booking details.')
        return redirect(url_for('main.login'))
    
    booking = Booking.query.get_or_404(booking_id)
    
    # Security: ensure user can only view their own bookings
    if booking.client_id != session['user_id'] and booking.photographer_id != session['user_id']:
        flash('You do not have permission to view this booking.')
        return redirect(url_for('bookings.bookings'))
    
    photographer = User.query.get(booking.photographer_id)
    client = User.query.get(booking.client_id)
    
    return render_template('booking_detail.html', booking=booking, photographer=photographer, client=client)


@bookings_bp.route('/bookings/<booking_id>/update', methods=['POST'])
def update_booking(booking_id):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    booking = Booking.query.get_or_404(booking_id)
    
    # Only photographer or client can update
    if booking.client_id != session['user_id'] and booking.photographer_id != session['user_id']:
        flash('You do not have permission to update this booking.')
        return redirect(url_for('bookings.bookings'))
    
    # Update booking details
    new_date = request.form.get('date')
    new_time = request.form.get('time')
    new_description = request.form.get('description')
    
    if new_date and new_time:
        booking.booking_date_and_time = datetime.strptime(f"{new_date} {new_time}", '%Y-%m-%d %H:%M')
    if new_description:
        booking.description = new_description
    
    booking.updated_at = datetime.utcnow()
    db.session.commit()
    
    flash('Booking updated successfully.')
    return redirect(url_for('bookings.booking_detail', booking_id=booking_id))
