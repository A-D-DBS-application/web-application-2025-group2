from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User, Photo, PhotographerAvailability, Album
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Get photographers from database
    photographers = User.query.filter_by(role='photographer').all()
    photographer_photos = {}
    for photographer in photographers:
        photos = Photo.query.filter_by(photographer_id=photographer.id).all()
        photographer_photos[photographer.id] = photos
    return render_template('index.html', photographers=photographers, photographer_photos=photographer_photos)

@main_bp.route('/register', methods=['GET', 'POST'])
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

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_role'] = user.role
            return redirect(url_for('main.index'))
        else:
            error = "Invalid email or password."

    return render_template('login.html', error=error)

@main_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('You have been logged out successfully.')
    return redirect(url_for('main.index'))

@main_bp.route('/photographers')
def photographers():
    """Browse all photographers with intelligent ranking"""
    from app.algorithms import rank_photographers, get_photographer_stats
    
    # Get optional search parameters
    event_type = request.args.get('event_type')
    desired_date_str = request.args.get('date')
    
    # Get current user if logged in
    client_id = None
    if 'user_id' in session:
        client_id = session['user_id']
    
    # Parse desired date if provided
    desired_date = None
    if desired_date_str:
        try:
            from datetime import datetime
            desired_date = datetime.strptime(desired_date_str, '%Y-%m-%d').date()
        except ValueError:
            pass
    
    # Get ranked photographers using the algorithm (with client_id for personalized ranking)
    ranked_photographers = rank_photographers(
        event_type=event_type,
        desired_date=desired_date,
        client_id=client_id
    )
    
    photographer_data = []
    for photographer, score, breakdown in ranked_photographers:
        photos = Photo.query.filter_by(photographer_id=photographer.id).limit(4).all()
        stats = get_photographer_stats(photographer.id)
        
        photographer_data.append({
            'id': photographer.id,
            'name': photographer.name,
            'email': photographer.email,
            'photos': [{'url': photo.image_url, 'id': photo.id} for photo in photos],
            'relevance_score': round(score, 1),
            'score_breakdown': breakdown,
            'stats': stats
        })
    
    return render_template('photographers.html', 
                         photographers=photographer_data,
                         event_type=event_type,
                         desired_date=desired_date_str)

@main_bp.route('/photographer/<int:photographer_id>')
def photographer_profile(photographer_id):
    photographer = User.query.get_or_404(photographer_id)
    photographer_photos = Photo.query.filter_by(photographer_id=photographer_id).all()
    return render_template('photographer_profile.html', photographer=photographer, photographer_photos=photographer_photos)

@main_bp.route('/api/photographer-slots/<int:photographer_id>')
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

@main_bp.route('/portfolio/<int:photographer_id>')
def view_portfolio(photographer_id):
    """Public portfolio view for clients"""
    photographer = User.query.get_or_404(photographer_id)
    if photographer.role != 'photographer':
        flash('User is not a photographer', 'danger')
        return redirect(url_for('main.index'))
    
    albums = Album.query.filter_by(photographer_id=photographer_id).order_by(Album.created_at.desc()).all()
    total_photos = sum(len(album.photos) for album in albums)
    
    return render_template('portfolio.html', 
                         photographer=photographer, 
                         albums=albums,
                         total_photos=total_photos)

