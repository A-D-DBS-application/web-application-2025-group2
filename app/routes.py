# app/routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User, Booking
from datetime import datetime

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

@main.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('main.index'))

@main.route('/book', methods=['GET', 'POST'])
def book():
    # Check if user is logged in
    if 'user_id' not in session:
        flash('Please log in to book a photographer.')
        return redirect(url_for('main.login'))
    
    if request.method == 'POST':
        photographer = request.form.get('photographer')
        date = request.form.get('date')
        time = request.form.get('time')
        name = request.form.get('name')
        email = request.form.get('email')
        notes = request.form.get('notes')
        
        # Combine date and time
        booking_datetime = datetime.strptime(f"{date} {time}", '%Y-%m-%d %H:%M')
        
        # Get photographer_id (hardcoded for now, you'll need to map photographer names to IDs)
        photographer_map = {
            'emma': 1,
            'lars': 2,
            'sophie': 3
        }
        photographer_id = photographer_map.get(photographer, 1)
        
        # Get client_id from logged-in user
        client_id = session['user_id']
        
        if not client_id:
            flash('You must be logged in to book a photographer.')
            return redirect(url_for('main.login'))
        
        new_booking = Booking(
            client_id=client_id,  # Now has a valid integer value
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
    
    return render_template('book.html')
