from flask import current_app, session
from supabase import create_client, Client
from app.models import User

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
