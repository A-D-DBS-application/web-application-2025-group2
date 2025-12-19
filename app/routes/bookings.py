from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import User, Booking, PhotographerAvailability, Album
from app.utils.helpers import get_unique_album_types
from datetime import datetime
from app.utils.decorators import login_required
from app.utils.dashboard_helpers import get_booking_with_security_check

bookings_bp = Blueprint('bookings', __name__)

@bookings_bp.route('/book', methods=['GET', 'POST'])
@login_required
def book():
    if request.method == 'POST':
        photographer_id, slot_id = request.form.get('photographer_id'), request.form.get('slot_id')
        
        if not photographer_id or not slot_id:
            flash('Please select a photographer and time slot.')
            return redirect(url_for('bookings.book'))
        
        slot = PhotographerAvailability.query.get(slot_id)
        if not slot or slot.photographer_id != int(photographer_id) or not slot.is_available:
            flash('Invalid or unavailable time slot.')
            return redirect(url_for('bookings.book'))
        
        booking_datetime = datetime.combine(slot.available_date, datetime.strptime(slot.start_time, '%H:%M').time())
        
        booking_type = request.form.get('booking_type') or 'session'
        
        new_booking = Booking(client_id=session['user_id'], photographer_id=int(photographer_id),
                            booking_date_and_time=booking_datetime, type=booking_type, 
                            description=request.form.get('notes'))
        
        db.session.add(new_booking)
        slot.is_available = False
        db.session.commit()
        
        return redirect(url_for('bookings.booking_confirmation', booking_id=new_booking.id))
    
    photographers = User.query.filter_by(role='photographer').all()
    album_types = get_unique_album_types()
    return render_template('book.html', photographers={p.id: {'name': p.name, 'id': p.id} for p in photographers}, album_types=album_types)

@bookings_bp.route('/booking-confirmation/<booking_id>')
@login_required
def booking_confirmation(booking_id):
    booking = Booking.query.get(booking_id)
    if not booking or booking.client_id != session['user_id']:
        flash('Booking not found.')
        return redirect(url_for('main.index'))
    
    photographer = User.query.get(booking.photographer_id)
    return render_template('booking_confirmation.html', booking=booking,
                         photographer_name=photographer.name if photographer else 'Unknown')

@bookings_bp.route('/bookings')
@login_required
def bookings():
    user = User.query.get(session['user_id'])
    user_bookings = Booking.query.filter_by(
        photographer_id=user.id if user.role == 'photographer' else None,
        client_id=user.id if user.role != 'photographer' else None
    ).order_by(Booking.booking_date_and_time.desc()).all()
    return render_template('bookings.html', bookings=user_bookings, user=user)


@bookings_bp.route('/bookings/<booking_id>')
@login_required
def booking_detail(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    
    if booking.client_id != session['user_id'] and booking.photographer_id != session['user_id']:
        flash('You do not have permission to view this booking.')
        return redirect(url_for('bookings.bookings'))
    
    return render_template('booking_detail.html', booking=booking,
                         photographer=User.query.get(booking.photographer_id),
                         client=User.query.get(booking.client_id))


@bookings_bp.route('/bookings/<booking_id>/update', methods=['POST'])
@login_required
def update_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    
    if booking.client_id != session['user_id'] and booking.photographer_id != session['user_id']:
        flash('You do not have permission to update this booking.')
        return redirect(url_for('bookings.bookings'))
    
    new_date, new_time = request.form.get('date'), request.form.get('time')
    if new_date and new_time:
        booking.booking_date_and_time = datetime.strptime(f"{new_date} {new_time}", '%Y-%m-%d %H:%M')
    if request.form.get('description'):
        booking.description = request.form.get('description')
    
    booking.updated_at = datetime.utcnow()
    db.session.commit()
    
    flash('Booking updated successfully.')
    return redirect(url_for('bookings.booking_detail', booking_id=booking_id))
