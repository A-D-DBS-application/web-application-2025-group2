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
    'style_match': 0.30,      # Portfolio matches event type
    'availability': 0.25,      # Has slots near desired date
    'performance': 0.20,       # Completion rate and ratings
    'price_match': 0.15,       # Within budget (future)
    'recency': 0.10           # Recently active
}

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
