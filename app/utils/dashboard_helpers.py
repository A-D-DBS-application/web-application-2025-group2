"""Helper functions for dashboard operations"""
from app.models import User, Booking, Photo
from flask import flash, redirect, url_for

def get_booking_with_security_check(booking_id, user, allowed_roles=None):
    """Get booking and check if user has access"""
    booking = Booking.query.get_or_404(booking_id)
    
    if allowed_roles == 'client' and booking.client_id != user.id:
        flash('You can only access your own bookings.')
        return None, redirect(url_for('dashboard.client_dashboard'))
    
    if allowed_roles == 'photographer' and booking.photographer_id != user.id:
        flash('You can only access your own bookings.')
        return None, redirect(url_for('dashboard.photographer_dashboard'))
    
    if allowed_roles == 'both' and booking.client_id != user.id and booking.photographer_id != user.id:
        flash('Access denied.')
        return None, redirect(url_for('main.index'))
    
    return booking, None

def enrich_bookings_with_details(bookings, for_photographer=True):
    """Add client/photographer and photo count to bookings"""
    for booking in bookings:
        if for_photographer:
            booking.client = User.query.get(booking.client_id)
        else:
            booking.photographer = User.query.get(booking.photographer_id)
        booking.photo_count = Photo.query.filter_by(booking_id=booking.id).count()
    return bookings

def free_availability_slot(booking):
    """Free up availability slot when booking is cancelled/rescheduled"""
    from app.models import PhotographerAvailability
    from app import db
    
    if booking.booking_date_and_time:
        slot = PhotographerAvailability.query.filter_by(
            photographer_id=booking.photographer_id,
            available_date=booking.booking_date_and_time.date(),
            is_available=False
        ).first()
        
        if slot:
            slot.is_available = True
            db.session.commit()
