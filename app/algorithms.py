"""
Smart photographer ranking and matching algorithms.

This module implements intelligent photographer ranking based on multiple factors:
- Portfolio style matching (albums relevant to event type)
- Availability near desired date
- Past performance (completion rate, ratings)
- Recency (recently active photographers)
"""

from datetime import datetime, timedelta
from sqlalchemy import func, and_
from app.models import User, Album, Booking, Photo, PhotographerAvailability, Rating, db
from app.constants import (
    RANKING_WEIGHTS, 
    BOOKING_STATUS_COMPLETED, 
    BOOKING_STATUS_CANCELLED,
    ROLE_PHOTOGRAPHER
)


def calculate_style_match_score(photographer, event_type):
    """
    Calculate how well photographer's portfolio matches the event type.
    
    Args:
        photographer: User object with role='photographer'
        event_type: String like 'wedding', 'portrait', 'corporate', etc.
    
    Returns:
        float: Score from 0-100
    """
    if not event_type:
        return 50  # Neutral score if no event type specified
    
    # Get all albums for this photographer
    albums = Album.query.filter_by(photographer_id=photographer.id).all()
    
    if not albums:
        return 0  # No portfolio = 0 score
    
    # Check if any album name/description contains event type keywords
    event_keywords = event_type.lower().split()
    matching_albums = 0
    total_photos = 0
    
    for album in albums:
        album_text = f"{album.name} {album.description or ''}".lower()
        if any(keyword in album_text for keyword in event_keywords):
            matching_albums += 1
            # Count photos in matching albums
            total_photos += len(album.photos)
    
    if matching_albums == 0:
        return 20  # Has portfolio but no matching albums
    
    # Score based on both number of matching albums and their size
    match_ratio = matching_albums / len(albums)
    photo_bonus = min(total_photos * 2, 30)  # Up to 30 bonus points for photos
    
    return min(match_ratio * 70 + photo_bonus, 100)


def calculate_availability_score(photographer, desired_date=None):
    """
    Calculate photographer's availability score.
    
    Args:
        photographer: User object
        desired_date: datetime.date object or None
    
    Returns:
        float: Score from 0-100
    """
    today = datetime.now().date()
    
    # Get all future available slots
    future_slots = PhotographerAvailability.query.filter(
        PhotographerAvailability.photographer_id == photographer.id,
        PhotographerAvailability.available_date >= today,
        PhotographerAvailability.is_available == True
    ).count()
    
    if future_slots == 0:
        return 0  # No availability
    
    base_score = min(future_slots * 10, 60)  # Up to 60 points for having slots
    
    # Bonus if has availability near desired date
    if desired_date:
        date_range_start = desired_date - timedelta(days=7)
        date_range_end = desired_date + timedelta(days=7)
        
        nearby_slots = PhotographerAvailability.query.filter(
            PhotographerAvailability.photographer_id == photographer.id,
            PhotographerAvailability.available_date >= date_range_start,
            PhotographerAvailability.available_date <= date_range_end,
            PhotographerAvailability.is_available == True
        ).count()
        
        if nearby_slots > 0:
            base_score += 40  # Big bonus for availability near desired date
    
    return min(base_score, 100)


def calculate_performance_score(photographer):
    """
    Calculate photographer's performance score based on bookings and ratings.
    
    Args:
        photographer: User object
    
    Returns:
        float: Score from 0-100
    """
    # Get all bookings for this photographer
    total_bookings = Booking.query.filter_by(photographer_id=photographer.id).count()
    
    if total_bookings == 0:
        return 50  # New photographer, neutral score
    
    # Calculate completion rate
    completed_bookings = Booking.query.filter_by(
        photographer_id=photographer.id,
        status=BOOKING_STATUS_COMPLETED
    ).count()
    
    completion_rate = completed_bookings / total_bookings if total_bookings > 0 else 0
    
    # Calculate average rating
    avg_rating_result = db.session.query(func.avg(Rating.rating)).filter(
        Rating.photographer_id == photographer.id
    ).scalar()
    
    avg_rating = float(avg_rating_result) if avg_rating_result else None
    
    # Build score
    completion_score = completion_rate * 50  # Up to 50 points
    
    if avg_rating:
        rating_score = (avg_rating / 5.0) * 50  # Up to 50 points (5 stars = 50)
    else:
        rating_score = 25  # Neutral if no ratings yet
    
    return min(completion_score + rating_score, 100)


def calculate_recency_score(photographer):
    """
    Calculate how recently the photographer has been active.
    
    Args:
        photographer: User object
    
    Returns:
        float: Score from 0-100
    """
    today = datetime.now()
    
    # Find most recent activity (booking or photo upload)
    latest_booking = Booking.query.filter_by(
        photographer_id=photographer.id
    ).order_by(Booking.created_at.desc()).first()
    
    latest_photo = Photo.query.filter_by(
        photographer_id=photographer.id
    ).order_by(Photo.uploaded_at.desc()).first()
    
    # Get most recent activity date
    latest_activity = None
    
    if latest_booking and latest_photo:
        # Handle timezone-aware and timezone-naive datetime comparison
        booking_time = latest_booking.created_at.replace(tzinfo=None) if latest_booking.created_at.tzinfo else latest_booking.created_at
        photo_time = latest_photo.uploaded_at.replace(tzinfo=None) if latest_photo.uploaded_at.tzinfo else latest_photo.uploaded_at
        latest_activity = max(booking_time, photo_time)
    elif latest_booking:
        latest_activity = latest_booking.created_at.replace(tzinfo=None) if latest_booking.created_at.tzinfo else latest_booking.created_at
    elif latest_photo:
        latest_activity = latest_photo.uploaded_at.replace(tzinfo=None) if latest_photo.uploaded_at.tzinfo else latest_photo.uploaded_at
    else:
        # No activity, check account creation
        return 30  # Low score for inactive photographers
    
    # Calculate days since last activity (ensure both are naive)
    today_naive = today.replace(tzinfo=None) if today.tzinfo else today
    days_since_activity = (today_naive - latest_activity).days
    
    if days_since_activity <= 7:
        return 100  # Very active
    elif days_since_activity <= 30:
        return 80  # Active this month
    elif days_since_activity <= 90:
        return 60  # Active this quarter
    elif days_since_activity <= 180:
        return 40  # Active this half year
    else:
        return 20  # Inactive


def rank_photographers(event_type=None, desired_date=None, limit=None):
    """
    Main function to rank all photographers based on 3 key factors:
    - Style match (40%): Portfolio relevance to event type
    - Availability (30%): Has slots near desired date
    - Performance (30%): Completion rate and ratings
    
    Args:
        event_type: String like 'wedding', 'portrait', etc. (optional)
        desired_date: datetime.date object (optional)
        limit: Maximum number of photographers to return (optional)
    
    Returns:
        List of tuples: [(photographer, score, breakdown), ...]
        sorted by score descending
    """
    # Get all photographers
    photographers = User.query.filter_by(role=ROLE_PHOTOGRAPHER).all()
    
    ranked_photographers = []
    
    for photographer in photographers:
        # Calculate individual scores (only 3 factors)
        style_score = calculate_style_match_score(photographer, event_type)
        availability_score = calculate_availability_score(photographer, desired_date)
        performance_score = calculate_performance_score(photographer)
        
        # Calculate weighted total score (40% + 30% + 30% = 100%)
        total_score = (
            style_score * RANKING_WEIGHTS['style_match'] +
            availability_score * RANKING_WEIGHTS['availability'] +
            performance_score * RANKING_WEIGHTS['performance']
        )
        
        # Score breakdown for debugging/display
        breakdown = {
            'style_match': round(style_score, 1),
            'availability': round(availability_score, 1),
            'performance': round(performance_score, 1),
            'total': round(total_score, 1)
        }
        
        ranked_photographers.append((photographer, total_score, breakdown))
    
    # Sort by total score descending
    ranked_photographers.sort(key=lambda x: x[1], reverse=True)
    
    # Apply limit if specified
    if limit:
        ranked_photographers = ranked_photographers[:limit]
    
    return ranked_photographers


def get_photographer_stats(photographer_id):
    """
    Get detailed statistics for a photographer.
    
    Args:
        photographer_id: Integer user ID
    
    Returns:
        dict: Statistics including ratings, bookings, completion rate
    """
    photographer = User.query.get(photographer_id)
    
    if not photographer or photographer.role != ROLE_PHOTOGRAPHER:
        return None
    
    # Bookings stats
    total_bookings = Booking.query.filter_by(photographer_id=photographer_id).count()
    completed_bookings = Booking.query.filter_by(
        photographer_id=photographer_id,
        status=BOOKING_STATUS_COMPLETED
    ).count()
    
    completion_rate = (completed_bookings / total_bookings * 100) if total_bookings > 0 else 0
    
    # Ratings stats
    ratings_count = Rating.query.filter_by(photographer_id=photographer_id).count()
    avg_rating = db.session.query(func.avg(Rating.rating)).filter(
        Rating.photographer_id == photographer_id
    ).scalar()
    
    # Portfolio stats
    albums_count = Album.query.filter_by(photographer_id=photographer_id).count()
    photos_count = Photo.query.filter_by(photographer_id=photographer_id).count()
    
    # Availability
    available_slots = PhotographerAvailability.query.filter(
        PhotographerAvailability.photographer_id == photographer_id,
        PhotographerAvailability.available_date >= datetime.now().date(),
        PhotographerAvailability.is_available == True
    ).count()
    
    return {
        'total_bookings': total_bookings,
        'completed_bookings': completed_bookings,
        'completion_rate': round(completion_rate, 1),
        'ratings_count': ratings_count,
        'average_rating': round(float(avg_rating), 1) if avg_rating else None,
        'albums_count': albums_count,
        'photos_count': photos_count,
        'available_slots': available_slots
    }
