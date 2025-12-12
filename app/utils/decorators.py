from functools import wraps
from flask import session, flash, redirect, url_for
from app.models import User
from app.constants import ROLE_PHOTOGRAPHER

def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function

def photographer_required(f):
    """Decorator to require photographer role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('main.login'))
        
        user = User.query.get(session['user_id'])
        if not user or user.role != ROLE_PHOTOGRAPHER:
            flash('Access denied. Photographers only.', 'danger')
            return redirect(url_for('main.index'))
        
        return f(*args, **kwargs)
    return decorated_function
