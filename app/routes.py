# app/routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import Client, Booking
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if 'user_id' in session:
        user = Client.query.get(session['user_id'])
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
        elif db.session.query(Client).filter_by(email=email).first():
            error = "Email already registered."
        else:
            hashed_pw = generate_password_hash(password)
            new_client = Client(
                name=name,
                email=email,
                password_hash=hashed_pw,
                role='client'  # Use one of the allowed values
            )
            db.session.add(new_client)
            db.session.commit()
            return redirect(url_for('main.login'))

    return render_template('register.html', error=error)

@main.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']

        client = Client.query.filter_by(email=email).first()
        
        if client and check_password_hash(client.password_hash, password):
            session['user_id'] = client.id
            session['user_name'] = client.name
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
    if request.method == 'POST':
        photographer = request.form.get('photographer')
        date = request.form.get('date')
        time = request.form.get('time')
        name = request.form.get('name')
        email = request.form.get('email')
        notes = request.form.get('notes')

        # Basic validation
        if not (photographer and date and time and name and email):
            error = 'Please fill in all required fields.'
            return render_template('book.html', error=error)

        # combine date and time into a datetime object
        try:
            booking_dt = datetime.fromisoformat(f"{date}T{time}")
        except Exception:
            error = 'Invalid date or time format.'
            return render_template('book.html', error=error)

        # photographer field contains an integer id from the select
        try:
            photographer_id = int(photographer)
        except ValueError:
            error = 'Invalid photographer selected.'
            return render_template('book.html', error=error)

        # create Booking record and save to DB (Supabase)
        new_booking = Booking(
            photographer_id=photographer_id,
            booking_date=booking_dt,
            type='session',
            description=notes,
            status='pending'
        )
        db.session.add(new_booking)
        db.session.commit()

        success = 'Your booking request has been sent. The photographer will contact you shortly.'
        return render_template('book.html', success=success)

    return render_template('book.html')
