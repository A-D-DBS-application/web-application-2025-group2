from flask import current_app, session
from supabase import create_client, Client
from app.models import User, Album, db
from app.constants import ALBUM_CATEGORIES

def get_supabase_client() -> Client:
    """Create and return Supabase client"""
    url = current_app.config['SUPABASE_URL']
    key = current_app.config['SUPABASE_KEY']
    return create_client(url, key)

def get_current_user():
    """Helper to get current logged-in user"""
    if 'user_id' not in session:
        return None
    return User.query.get(session['user_id'])

def get_unique_album_types(photographer_id=None):
    """
    Get a normalized list of album types/categories from existing albums.
    Groups similar names (e.g., 'Wedding', 'Weddings', 'Wedding Photography') 
    into single categories.
    """
    # Get all unique album names
    query = db.session.query(Album.name).distinct()
    if photographer_id:
        query = query.filter(Album.photographer_id == photographer_id)
        
    raw_names = [r[0] for r in query.all()]
    
    normalized_types = set()
    
    for name in raw_names:
        if not name: continue
        name_lower = name.lower()
        matched = False
        
        # Check against standard categories
        for category, keywords in ALBUM_CATEGORIES.items():
            if any(k in name_lower for k in keywords):
                normalized_types.add(category)
                matched = True
        
        # If no standard category matched, add the original name formatted
        if not matched:
            normalized_types.add(name.strip())
            
    return sorted(list(normalized_types))

