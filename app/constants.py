"""
Application constants for the photography booking platform.
"""

# Booking statuses
BOOKING_STATUS_PENDING = 'pending'
BOOKING_STATUS_CONFIRMED = 'confirmed'
BOOKING_STATUS_COMPLETED = 'completed'
BOOKING_STATUS_CANCELLED = 'cancelled'

BOOKING_STATUSES = [
    BOOKING_STATUS_PENDING,
    BOOKING_STATUS_CONFIRMED,
    BOOKING_STATUS_COMPLETED,
    BOOKING_STATUS_CANCELLED
]

# User roles
ROLE_PHOTOGRAPHER = 'photographer'
ROLE_CLIENT = 'user'

USER_ROLES = [ROLE_PHOTOGRAPHER, ROLE_CLIENT]

# Storage paths
STORAGE_PATH_ALBUMS = 'albums'
STORAGE_PATH_BOOKINGS = 'bookings'

# Allowed file extensions for uploads
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Ranking algorithm weights
RANKING_WEIGHTS = {
    'style_match': 0.35,       # Portfolio matches event type (35%)
    'availability': 0.25,      # Has slots near desired date (25%)
    'performance': 0.25,       # Completion rate and ratings (25%)
    'delivery_speed': 0.15,    # Photo delivery speed (15%)
}

# Style match scoring
STYLE_MATCH_BASE_WEIGHT = 70
STYLE_MATCH_PHOTO_BONUS_PER_MATCH = 2
STYLE_MATCH_PHOTO_BONUS_MAX = 30
STYLE_MATCH_NO_MATCH_SCORE = 20
STYLE_MATCH_NO_ALBUMS_SCORE = 0
STYLE_MATCH_NO_EVENT_TYPE_SCORE = 50

# Availability scoring
AVAILABILITY_POINTS_PER_SLOT = 10
AVAILABILITY_BASE_MAX = 60
AVAILABILITY_NEARBY_BONUS = 40
AVAILABILITY_NEARBY_DAYS_RANGE = 7
AVAILABILITY_NO_SLOTS_SCORE = 0

# Performance scoring
PERFORMANCE_COMPLETION_WEIGHT = 50
PERFORMANCE_RATING_WEIGHT = 50
PERFORMANCE_NO_BOOKINGS_SCORE = 50
PERFORMANCE_NO_RATING_DEFAULT = 25
PERFORMANCE_MAX_RATING = 5.0

# Client history bonus
CLIENT_HISTORY_BONUS_MAX = 30
CLIENT_HISTORY_RATING_WEIGHT = 20
CLIENT_HISTORY_REPEAT_POINTS = 2
CLIENT_HISTORY_REPEAT_MAX = 10
CLIENT_HISTORY_NO_RATING_BONUS = 5

# Photo delivery speed scoring (days -> score)
DELIVERY_SPEED_THRESHOLDS = {
    0: 100,    # Same day
    2: 90,     # Within 2 days
    5: 80,     # Within 5 days
    7: 70,     # Within a week
    14: 60,    # Within 2 weeks
    30: 40,    # Within a month
}
DELIVERY_SPEED_DEFAULT_SCORE = 20  # Over 30 days
DELIVERY_SPEED_NO_DATA_SCORE = 50

# Event types for bookings
EVENT_TYPES = [
    'wedding',
    'portrait',
    'corporate',
    'funeral',
    'birthday',
    'product',
    'event',
    'other'
]
