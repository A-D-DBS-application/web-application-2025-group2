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
    ROLE_PHOTOGRAPHER,
    STYLE_MATCH_BASE_WEIGHT,
    STYLE_MATCH_PHOTO_BONUS_PER_MATCH,
    STYLE_MATCH_PHOTO_BONUS_MAX,
    STYLE_MATCH_NO_MATCH_SCORE,
    STYLE_MATCH_NO_ALBUMS_SCORE,
    STYLE_MATCH_NO_EVENT_TYPE_SCORE,
    AVAILABILITY_POINTS_PER_SLOT,
    AVAILABILITY_BASE_MAX,
    AVAILABILITY_NEARBY_BONUS,
    AVAILABILITY_NEARBY_DAYS_RANGE,
    AVAILABILITY_NO_SLOTS_SCORE,
    PERFORMANCE_COMPLETION_WEIGHT,
    PERFORMANCE_RATING_WEIGHT,
    PERFORMANCE_NO_BOOKINGS_SCORE,
    PERFORMANCE_NO_RATING_DEFAULT,
    PERFORMANCE_MAX_RATING,
    CLIENT_HISTORY_BONUS_MAX,
    CLIENT_HISTORY_RATING_WEIGHT,
    CLIENT_HISTORY_REPEAT_POINTS,
    CLIENT_HISTORY_REPEAT_MAX,
    CLIENT_HISTORY_NO_RATING_BONUS,
    DELIVERY_SPEED_THRESHOLDS,
    DELIVERY_SPEED_DEFAULT_SCORE,
    DELIVERY_SPEED_NO_DATA_SCORE
)


def calculate_style_match_score(photographer, event_type):
    """Calculate portfolio match score (0-100)"""
    if not event_type:
        return STYLE_MATCH_NO_EVENT_TYPE_SCORE
    
    albums = Album.query.filter_by(photographer_id=photographer.id).all()
    if not albums:
        return STYLE_MATCH_NO_ALBUMS_SCORE
    
    keywords = event_type.lower().split()
    matching_albums = sum(1 for a in albums if any(k in f"{a.name} {a.description or ''}".lower() for k in keywords))
    
    if matching_albums == 0:
        return STYLE_MATCH_NO_MATCH_SCORE
    
    match_ratio = matching_albums / len(albums)
    photo_bonus = min(sum(len(a.photos) for a in albums if any(k in f"{a.name} {a.description or ''}".lower() for k in keywords)) * STYLE_MATCH_PHOTO_BONUS_PER_MATCH, STYLE_MATCH_PHOTO_BONUS_MAX)
    
    return min(match_ratio * STYLE_MATCH_BASE_WEIGHT + photo_bonus, 100)


def calculate_availability_score(photographer, desired_date=None):
    """Calculate availability score (0-100)"""
    today = datetime.now().date()
    future_slots = PhotographerAvailability.query.filter(
        PhotographerAvailability.photographer_id == photographer.id,
        PhotographerAvailability.available_date >= today,
        PhotographerAvailability.is_available == True
    ).count()
    
    if future_slots == 0:
        return AVAILABILITY_NO_SLOTS_SCORE
    
    base_score = min(future_slots * AVAILABILITY_POINTS_PER_SLOT, AVAILABILITY_BASE_MAX)
    
    if desired_date:
        nearby_slots = PhotographerAvailability.query.filter(
            PhotographerAvailability.photographer_id == photographer.id,
            PhotographerAvailability.available_date.between(desired_date - timedelta(days=AVAILABILITY_NEARBY_DAYS_RANGE), desired_date + timedelta(days=AVAILABILITY_NEARBY_DAYS_RANGE)),
            PhotographerAvailability.is_available == True
        ).count()
        
        if nearby_slots > 0:
            base_score += AVAILABILITY_NEARBY_BONUS
    
    return min(base_score, 100)


def calculate_performance_score(photographer):
    """Calculate performance score (0-100)"""
    total_bookings = Booking.query.filter_by(photographer_id=photographer.id).count()
    if total_bookings == 0:
        return PERFORMANCE_NO_BOOKINGS_SCORE
    
    completed = Booking.query.filter_by(photographer_id=photographer.id, status=BOOKING_STATUS_COMPLETED).count()
    avg_rating = db.session.query(func.avg(Rating.rating)).filter(Rating.photographer_id == photographer.id).scalar()
    
    completion_score = (completed / total_bookings) * PERFORMANCE_COMPLETION_WEIGHT
    rating_score = (float(avg_rating) / PERFORMANCE_MAX_RATING * PERFORMANCE_RATING_WEIGHT) if avg_rating else PERFORMANCE_NO_RATING_DEFAULT
    
    return min(completion_score + rating_score, 100)


def calculate_client_history_bonus(photographer, client_id):
    """Calculate client history bonus (0-30)"""
    if not client_id:
        return 0
    
    previous_bookings = Booking.query.filter_by(
        client_id=client_id, photographer_id=photographer.id, status=BOOKING_STATUS_COMPLETED
    ).all()
    
    if not previous_bookings:
        return 0
    
    ratings = Rating.query.filter_by(client_id=client_id, photographer_id=photographer.id).all()
    if not ratings:
        return CLIENT_HISTORY_NO_RATING_BONUS
    
    avg_rating = sum(r.rating for r in ratings) / len(ratings)
    bonus = (avg_rating / PERFORMANCE_MAX_RATING) * CLIENT_HISTORY_RATING_WEIGHT
    
    if len(previous_bookings) > 1:
        bonus += min(len(previous_bookings) * CLIENT_HISTORY_REPEAT_POINTS, CLIENT_HISTORY_REPEAT_MAX)
    
    return min(bonus, CLIENT_HISTORY_BONUS_MAX)


def calculate_photo_delivery_speed_score(photographer):
    """Calculate delivery speed score (0-100)"""
    completed_bookings = Booking.query.filter_by(
        photographer_id=photographer.id, status=BOOKING_STATUS_COMPLETED
    ).all()
    
    if not completed_bookings:
        return DELIVERY_SPEED_NO_DATA_SCORE
    
    delivery_times = []
    for booking in completed_bookings:
        photos = Photo.query.filter_by(
            booking_id=booking.id, photographer_id=photographer.id
        ).order_by(Photo.uploaded_at.asc()).all()
        
        if photos:
            upload = photos[0].uploaded_at.replace(tzinfo=None) if photos[0].uploaded_at.tzinfo else photos[0].uploaded_at
            book_date = booking.booking_date_and_time.replace(tzinfo=None) if booking.booking_date_and_time.tzinfo else booking.booking_date_and_time
            days = (upload - book_date).days
            if days >= 0:
                delivery_times.append(days)
    
    if not delivery_times:
        return DELIVERY_SPEED_NO_DATA_SCORE
    
    avg_days = sum(delivery_times) / len(delivery_times)
    
    # Use threshold dict from constants
    for threshold_days in sorted(DELIVERY_SPEED_THRESHOLDS.keys()):
        if avg_days <= threshold_days:
            return DELIVERY_SPEED_THRESHOLDS[threshold_days]
    
    return DELIVERY_SPEED_DEFAULT_SCORE


def rank_photographers(event_type=None, desired_date=None, client_id=None, limit=None):
    """Rank photographers by style (35%), availability (25%), performance (25%), delivery speed (15%) + history bonus"""
    photographers = User.query.filter_by(role=ROLE_PHOTOGRAPHER).all()
    ranked = []
    
    for p in photographers:
        scores = {
            'style_match': calculate_style_match_score(p, event_type),
            'availability': calculate_availability_score(p, desired_date),
            'performance': calculate_performance_score(p),
            'delivery_speed': calculate_photo_delivery_speed_score(p)
        }
        
        total = (scores['style_match'] * RANKING_WEIGHTS['style_match'] + 
                scores['availability'] * RANKING_WEIGHTS['availability'] + 
                scores['performance'] * RANKING_WEIGHTS['performance'] + 
                scores['delivery_speed'] * RANKING_WEIGHTS['delivery_speed'])
        
        if client_id:
            bonus = calculate_client_history_bonus(p, client_id)
            total += bonus
            scores['history_bonus'] = round(bonus, 1)
        else:
            scores['history_bonus'] = 0
        
        scores = {k: round(v, 1) for k, v in scores.items()}
        scores['total'] = round(total, 1)
        ranked.append((p, total, scores))
    
    ranked.sort(key=lambda x: x[1], reverse=True)
    return ranked[:limit] if limit else ranked


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
