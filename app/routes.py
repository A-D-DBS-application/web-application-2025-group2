# app/routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User, Booking, PhotographerAvailability
from datetime import datetime, timedelta
import json

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return render_template('index.html', username=user.name if user else None)
    return render_template('index.html', username=None)

@main.route('/register', methods=['GET', 'POST'])
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

@main.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            return redirect(url_for('main.index'))
        else:
            error = "Invalid email or password."

    return render_template('login.html', error=error)

@main.route('/api/photographer-slots/<int:photographer_id>')
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

@main.route('/book', methods=['GET', 'POST'])
def book():
    # Check if user is logged in
    if 'user_id' not in session:
        flash('Please log in to book a photographer.')
        return redirect(url_for('main.login'))
    
    if request.method == 'POST':
        photographer_id = request.form.get('photographer_id')
        slot_id = request.form.get('slot_id')
        name = request.form.get('name')
        email = request.form.get('email')
        notes = request.form.get('notes')
        
        # Get the availability slot
        slot = PhotographerAvailability.query.get(slot_id)
        if not slot or slot.photographer_id != int(photographer_id):
            flash('Invalid time slot selected.')
            return redirect(url_for('main.book'))
        
        # Combine date and time
        booking_datetime = datetime.combine(slot.available_date, datetime.strptime(slot.start_time, '%H:%M').time())
        
        # Get client_id from logged-in user
        client_id = session['user_id']
        
        new_booking = Booking(
            client_id=client_id,
            photographer_id=photographer_id,
            booking_date=booking_datetime,
            type='session',
            description=notes,
            status='pending'
        )
        db.session.add(new_booking)
        db.session.commit()
        
        flash('Booking request submitted successfully!')
        return redirect(url_for('main.index'))
    
    # Get all photographers with their availability
    photographers_data = {}
    availability_data = {}
    
    # Map photographer IDs to names (you can get this from DB if needed)
    photographer_map = {
        1: {'name': 'Emma', 'id': 1},
        2: {'name': 'Lars', 'id': 2},
        3: {'name': 'Sophie', 'id': 3}
    }
    
    # Get availability for all photographers
    slots = PhotographerAvailability.query.filter(
        PhotographerAvailability.available_date >= datetime.now().date(),
        PhotographerAvailability.is_available == True
    ).all()
    
    for slot in slots:
        pid = slot.photographer_id
        if pid not in availability_data:
            availability_data[pid] = []
        availability_data[pid].append({
            'id': slot.id,
            'date': slot.available_date.isoformat(),
            'start_time': slot.start_time,
            'end_time': slot.end_time
        })
    
    return render_template('book.html', 
                         photographers=photographer_map,
                         availability=json.dumps(availability_data))
