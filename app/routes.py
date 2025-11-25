# app/routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User, Booking, PhotographerAvailability, Photographer
from datetime import datetime, timedelta
import json

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return render_template('index.html', username=user.name if user else None)
    return render_template('index.html', username=None)

@main.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip().lower()
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if not name or not email or not password or not confirm_password:
            error = "All fields are required."
        elif password != confirm_password:
            error = "Passwords do not match."
        elif db.session.query(User).filter_by(email=email).first():
            error = "Email already registered."
        else:
            hashed_pw = generate_password_hash(password)
            new_user = User(
                username=email,  # Use email as username
                name=name,
                email=email,
                password_hash=hashed_pw,
                role='user'
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('main.login'))

    return render_template('register.html', error=error)

@main.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            return redirect(url_for('main.index'))
        else:
            error = "Invalid email or password."

    return render_template('login.html', error=error)

@main.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('You have been logged out successfully.')
    return redirect(url_for('main.index'))

@main.route('/api/photographer-slots/<int:photographer_id>')
def get_photographer_slots(photographer_id):
    """API endpoint to get available slots for a photographer"""
    slots = PhotographerAvailability.query.filter(
        PhotographerAvailability.photographer_id == photographer_id,
        PhotographerAvailability.available_date >= datetime.now().date(),
        PhotographerAvailability.is_available == True
    ).order_by(PhotographerAvailability.available_date).all()
    
    return jsonify([{
        'id': slot.id,
        'date': slot.available_date.isoformat(),
        'start_time': slot.start_time,
        'end_time': slot.end_time,
        'display': f"{slot.available_date.strftime('%d-%m-%Y')} {slot.start_time}-{slot.end_time}"
    } for slot in slots])

@main.route('/book', methods=['GET', 'POST'])
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
            return redirect(url_for('main.book'))
        
        # Get the availability slot
        slot = PhotographerAvailability.query.get(slot_id)
        if not slot or slot.photographer_id != int(photographer_id):
            flash('Invalid time slot selected.')
            return redirect(url_for('main.book'))
        
        # Check if slot is still available
        if not slot.is_available:
            flash('This time slot is no longer available.')
            return redirect(url_for('main.book'))
        
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
        return redirect(url_for('main.booking_confirmation', booking_id=new_booking.id))
    
    # GET request - show form
    photographer_map = {
        1: {'name': 'Emma van Berg', 'id': 1},
        2: {'name': 'Lars de Vries', 'id': 2},
        3: {'name': 'Sophie Janssen', 'id': 3}
    }
    
    return render_template('book.html', photographers=photographer_map)

@main.route('/booking-confirmation/<booking_id>')
def booking_confirmation(booking_id):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    booking = Booking.query.get(booking_id)
    if not booking or booking.client_id != session['user_id']:
        flash('Booking not found.')
        return redirect(url_for('main.index'))
    
    photographer_names = {
        1: 'Emma van Berg',
        2: 'Lars de Vries',
        3: 'Sophie Janssen'
    }
    
    return render_template('booking_confirmation.html', 
                         booking=booking,
                         photographer_name=photographer_names.get(booking.photographer_id, 'Unknown'))

@main.route('/admin/add-availability', methods=['GET', 'POST'])
def add_availability():
    if request.method == 'POST':
        photographer_id = request.form.get('photographer_id')
        date = request.form.get('date')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        
        availability = PhotographerAvailability(
            photographer_id=photographer_id,
            available_date=datetime.strptime(date, '%Y-%m-%d').date(),
            start_time=start_time,
            end_time=end_time,
            is_available=True
        )
        db.session.add(availability)
        db.session.commit()
        
        flash('Availability added successfully!')
        return redirect(url_for('main.index'))
    
    photographers = Photographer.query.all()
    return render_template('add_availability.html', photographers=photographers)

@main.route('/bookings')
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


@main.route('/bookings/<booking_id>')
def booking_detail(booking_id):
    if 'user_id' not in session:
        flash('Please log in to view booking details.')
        return redirect(url_for('main.login'))
    
    booking = Booking.query.get_or_404(booking_id)
    
    # Security: ensure user can only view their own bookings
    if booking.client_id != session['user_id'] and booking.photographer_id != session['user_id']:
        flash('You do not have permission to view this booking.')
        return redirect(url_for('main.bookings'))
    
    photographer = Photographer.query.get(booking.photographer_id)
    client = User.query.get(booking.client_id)
    
    return render_template('booking_detail.html', booking=booking, photographer=photographer, client=client)


@main.route('/bookings/<booking_id>/cancel', methods=['POST'])
def cancel_booking(booking_id):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    booking = Booking.query.get_or_404(booking_id)
    
    # Only client or photographer can cancel
    if booking.client_id != session['user_id'] and booking.photographer_id != session['user_id']:
        flash('You do not have permission to cancel this booking.')
        return redirect(url_for('main.bookings'))
    
    # Delete the booking
    db.session.delete(booking)
    db.session.commit()
    
    flash('Booking cancelled successfully.')
    return redirect(url_for('main.bookings'))


@main.route('/bookings/<booking_id>/update', methods=['POST'])
def update_booking(booking_id):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    booking = Booking.query.get_or_404(booking_id)
    
    # Only photographer or client can update
    if booking.client_id != session['user_id'] and booking.photographer_id != session['user_id']:
        flash('You do not have permission to update this booking.')
        return redirect(url_for('main.bookings'))
    
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
    return redirect(url_for('main.booking_detail', booking_id=booking_id))
