# app/routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from app.models import db, User, Booking, PhotographerAvailability, Photo
from datetime import datetime, timedelta
import json
import os
import uuid
from supabase import create_client, Client

main = Blueprint('main', __name__)

def get_supabase_client() -> Client:
    """Create and return Supabase client"""
    url = current_app.config['SUPABASE_URL']
    key = current_app.config['SUPABASE_KEY']
    return create_client(url, key)

@main.route('/')
def index():
    photographers = User.query.filter_by(role='photographer').limit(3).all()
    photographer_photos = {}
    for photographer in photographers:
        photos = Photo.query.filter_by(photographer_id=photographer.id).order_by(Photo.uploaded_at.desc()).limit(4).all()
        photographer_photos[photographer.id] = photos
    
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return render_template('index.html', username=user.name if user else None, user=user, photographers=photographers, photographer_photos=photographer_photos)
    return render_template('index.html', username=None, user=None, photographers=photographers, photographer_photos=photographer_photos)

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
                username=email,
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
    session.clear()
    flash('You have been logged out successfully.')
    return redirect(url_for('main.index'))

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
    if 'user_id' not in session:
        flash('Please log in to book a photographer.')
        return redirect(url_for('main.login'))
    
    if request.method == 'POST':
        photographer_id = request.form.get('photographer_id')
        slot_id = request.form.get('slot_id')
        name = request.form.get('name')
        email = request.form.get('email')
        notes = request.form.get('notes')
        
        if not photographer_id or not slot_id:
            flash('Please select a photographer and time slot.')
            return redirect(url_for('main.book'))
        
        slot = PhotographerAvailability.query.get(slot_id)
        if not slot or slot.photographer_id != int(photographer_id):
            flash('Invalid time slot selected.')
            return redirect(url_for('main.book'))
        
        if not slot.is_available:
            flash('This time slot is no longer available.')
            return redirect(url_for('main.book'))
        
        booking_datetime = datetime.combine(
            slot.available_date, 
            datetime.strptime(slot.start_time, '%H:%M').time()
        )
        
        new_booking = Booking(
            client_id=session['user_id'],
            photographer_id=int(photographer_id),
            booking_date_and_time=booking_datetime,
            type='session',
            description=notes
        )
        db.session.add(new_booking)
        slot.is_available = False
        db.session.commit()
        
        return redirect(url_for('main.booking_confirmation', booking_id=new_booking.id))
    
    photographers = User.query.filter_by(role='photographer').all()
    photographer_map = {p.id: {'name': p.name, 'id': p.id} for p in photographers}
    
    return render_template('book.html', photographers=photographer_map)

@main.route('/booking-confirmation/<booking_id>')
def booking_confirmation(booking_id):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    booking = Booking.query.get(booking_id)
    if not booking or booking.client_id != session['user_id']:
        flash('Booking not found.')
        return redirect(url_for('main.index'))
    
    photographer = User.query.get(booking.photographer_id)
    photographer_name = photographer.name if photographer else 'Unknown'
    
    return render_template('booking_confirmation.html', 
                         booking=booking,
                         photographer_name=photographer_name)

@main.route('/bookings')
def bookings():
    if 'user_id' not in session:
        flash('Please log in to view bookings.')
        return redirect(url_for('main.login'))
    
    user = User.query.get(session['user_id'])
    
    if user.role == 'photographer':
        user_bookings = Booking.query.filter_by(photographer_id=user.id).order_by(Booking.booking_date_and_time.desc()).all()
    else:
        user_bookings = Booking.query.filter_by(client_id=user.id).order_by(Booking.booking_date_and_time.desc()).all()
    
    return render_template('bookings.html', bookings=user_bookings, user=user)

@main.route('/bookings/<booking_id>')
def booking_detail(booking_id):
    if 'user_id' not in session:
        flash('Please log in to view booking details.')
        return redirect(url_for('main.login'))
    
    booking = Booking.query.get_or_404(booking_id)
    
    if booking.client_id != session['user_id'] and booking.photographer_id != session['user_id']:
        flash('You do not have permission to view this booking.')
        return redirect(url_for('main.bookings'))
    
    photographer = User.query.get(booking.photographer_id)
    client = User.query.get(booking.client_id)
    
    return render_template('booking_detail.html', booking=booking, photographer=photographer, client=client)

@main.route('/bookings/<booking_id>/update', methods=['POST'])
def update_booking(booking_id):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    booking = Booking.query.get_or_404(booking_id)
    
    if booking.client_id != session['user_id'] and booking.photographer_id != session['user_id']:
        flash('You do not have permission to update this booking.')
        return redirect(url_for('main.bookings'))
    
    new_date = request.form.get('date')
    new_time = request.form.get('time')
    new_description = request.form.get('description')
    
    if new_date and new_time:
        booking.booking_date_and_time = datetime.strptime(f"{new_date} {new_time}", '%Y-%m-%d %H:%M')
    if new_description:
        booking.description = new_description
    
    booking.updated_at = datetime.utcnow()
    db.session.commit()
    
    flash('Booking updated successfully.')
    return redirect(url_for('main.booking_detail', booking_id=booking_id))

@main.route('/booking/cancel/<booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        return redirect(url_for('main.login'))
    
    booking = Booking.query.get_or_404(booking_id)
    
    if booking.client_id != user.id and booking.photographer_id != user.id:
        flash('You do not have permission to cancel this booking.')
        return redirect(url_for('main.bookings'))
    
    if booking.booking_date_and_time:
        slot = PhotographerAvailability.query.filter_by(
            photographer_id=booking.photographer_id,
            available_date=booking.booking_date_and_time.date(),
            is_available=False
        ).first()
        
        if slot:
            slot.is_available = True
    
    db.session.delete(booking)
    db.session.commit()
    
    flash('Booking cancelled successfully!')
    return redirect(url_for('main.bookings'))

@main.route('/admin/add-availability', methods=['GET', 'POST'])
def add_availability():
    if request.method == 'POST':
        photographer_id = request.form.get('photographer_id')
        date = request.form.get('date')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        
        availability = PhotographerAvailability(
            photographer_id=photographer_id,
            available_date=datetime.strptime(date, '%Y-%m-%d').date(),
            start_time=start_time,
            end_time=end_time,
            is_available=True
        )
        db.session.add(availability)
        db.session.commit()
        
        flash('Availability added successfully!')
        return redirect(url_for('main.index'))
    
    photographers = User.query.filter_by(role='photographer').all()
    return render_template('add_availability.html', photographers=photographers)

@main.route('/dashboard/photographer')
def photographer_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    user = User.query.get(session['user_id'])
    if not user or user.role != 'photographer':
        flash('Access denied. Photographers only.')
        return redirect(url_for('main.index'))
    
    bookings_as_photographer = Booking.query.filter_by(photographer_id=user.id).order_by(Booking.booking_date_and_time.desc()).all()
    bookings_as_client = Booking.query.filter_by(client_id=user.id).order_by(Booking.booking_date_and_time.desc()).all()
    
    photographer_names = {}
    for booking in bookings_as_client:
        if booking.photographer_id:
            photographer = User.query.get(booking.photographer_id)
            if photographer:
                photographer_names[booking.photographer_id] = photographer.name
    
    client_names = {}
    for booking in bookings_as_photographer:
        if booking.client_id:
            client = User.query.get(booking.client_id)
            if client:
                client_names[booking.client_id] = client.name
    
    availability_slots = PhotographerAvailability.query.filter_by(
        photographer_id=user.id
    ).order_by(PhotographerAvailability.available_date).all()
    
    photos_taken = Photo.query.filter_by(photographer_id=user.id).order_by(Photo.uploaded_at.desc()).all()
    
    photos_as_client = Photo.query.filter_by(user_id=user.id).order_by(Photo.uploaded_at.desc()).all()
    
    photos_by_photographer = {}
    for photo in photos_as_client:
        if photo.photographer_id not in photos_by_photographer:
            photographer = User.query.get(photo.photographer_id)
            photos_by_photographer[photo.photographer_id] = {
                'name': photographer.name if photographer else 'Unknown',
                'photos': []
            }
        photos_by_photographer[photo.photographer_id]['photos'].append(photo)
    
    return render_template('photographer_dashboard.html', 
                         user=user,
                         bookings_as_photographer=bookings_as_photographer,
                         bookings_as_client=bookings_as_client,
                         availability_slots=availability_slots,
                         photographer_names=photographer_names,
                         client_names=client_names,
                         photos_taken=photos_taken,
                         photos_by_photographer=photos_by_photographer)

@main.route('/photographer/add-availability', methods=['POST'])
def add_availability_slot():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    user = User.query.get(session['user_id'])
    if not user or user.role != 'photographer':
        flash('Access denied. Photographers only.')
        return redirect(url_for('main.index'))
    
    date = request.form.get('date')
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    
    if not date or not start_time or not end_time:
        flash('All fields are required.')
        return redirect(url_for('main.photographer_dashboard'))
    
    new_slot = PhotographerAvailability(
        photographer_id=user.id,
        available_date=datetime.strptime(date, '%Y-%m-%d').date(),
        start_time=start_time,
        end_time=end_time,
        is_available=True
    )
    db.session.add(new_slot)
    db.session.commit()
    
    flash('Availability slot added successfully!')
    return redirect(url_for('main.photographer_dashboard'))

@main.route('/dashboard/photographer/delete-slot/<int:slot_id>', methods=['POST'])
def delete_slot(slot_id):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    user = User.query.get(session['user_id'])
    if not user or user.role != 'photographer':
        flash('Access denied. Photographers only.')
        return redirect(url_for('main.index'))
    
    slot = PhotographerAvailability.query.get_or_404(slot_id)
    
    if slot.photographer_id != user.id:
        flash('You can only delete your own availability slots.')
        return redirect(url_for('main.photographer_dashboard'))
    
    if not slot.is_available:
        flash('Cannot delete a slot that has already been booked.')
        return redirect(url_for('main.photographer_dashboard'))
    
    db.session.delete(slot)
    db.session.commit()
    
    flash('Availability slot deleted successfully!')
    return redirect(url_for('main.photographer_dashboard'))

@main.route('/dashboard/client')
def client_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        return redirect(url_for('main.login'))
    
    bookings = Booking.query.filter_by(client_id=user.id).order_by(Booking.booking_date_and_time.desc()).all()
    
    photographer_names = {}
    for booking in bookings:
        if booking.photographer_id:
            photographer = User.query.get(booking.photographer_id)
            if photographer:
                photographer_names[booking.photographer_id] = photographer.name
    
    photos = Photo.query.filter_by(user_id=user.id).order_by(Photo.uploaded_at.desc()).all()
    
    photos_by_photographer = {}
    for photo in photos:
        if photo.photographer_id not in photos_by_photographer:
            photographer = User.query.get(photo.photographer_id)
            photos_by_photographer[photo.photographer_id] = {
                'name': photographer.name if photographer else 'Unknown',
                'photos': []
            }
        photos_by_photographer[photo.photographer_id]['photos'].append(photo)
    
    return render_template('client_dashboard.html',
                         user=user,
                         bookings=bookings,
                         photographer_names=photographer_names,
                         photos_by_photographer=photos_by_photographer)

@main.route('/dashboard/photographer/upload-photos/<booking_id>', methods=['GET', 'POST'])
def upload_photos(booking_id):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    user = User.query.get(session['user_id'])
    if not user or user.role != 'photographer':
        flash('Access denied. Photographers only.')
        return redirect(url_for('main.index'))
    
    booking = Booking.query.get_or_404(booking_id)
    
    if booking.photographer_id != user.id:
        flash('You can only upload photos for your own bookings.')
        return redirect(url_for('main.photographer_dashboard'))
    
    client = User.query.get(booking.client_id)
    
    if request.method == 'POST':
        photo_title = request.form.get('photo_title', '')
        
        if 'photo_file' not in request.files:
            flash('No file selected.')
            return redirect(url_for('main.upload_photos', booking_id=booking_id))
        
        file = request.files['photo_file']
        
        if file.filename == '':
            flash('No file selected.')
            return redirect(url_for('main.upload_photos', booking_id=booking_id))
        
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
        file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        
        if file_ext not in allowed_extensions:
            flash('Invalid file type. Please upload an image (PNG, JPG, JPEG, GIF, WEBP).')
            return redirect(url_for('main.upload_photos', booking_id=booking_id))
        
        try:
            unique_filename = f"{uuid.uuid4()}.{file_ext}"
            file_path = f"bookings/{booking_id}/{unique_filename}"
            
            supabase = get_supabase_client()
            bucket_name = current_app.config['SUPABASE_STORAGE_BUCKET']
            
            file_content = file.read()
            
            response = supabase.storage.from_(bucket_name).upload(
                file_path,
                file_content,
                file_options={"content-type": file.content_type}
            )
            
            photo_url = supabase.storage.from_(bucket_name).get_public_url(file_path)
            
            new_photo = Photo(
                user_id=booking.client_id,
                photographer_id=user.id,
                booking_id=booking.id,
                image_url=photo_url,
                title=photo_title or file.filename
            )
            db.session.add(new_photo)
            db.session.commit()
            
            flash('Photo uploaded successfully!')
            
        except Exception as e:
            flash(f'Error uploading photo: {str(e)}')
            return redirect(url_for('main.upload_photos', booking_id=booking_id))
        
        return redirect(url_for('main.upload_photos', booking_id=booking_id))
    
    existing_photos = Photo.query.filter_by(booking_id=booking.id).order_by(Photo.uploaded_at.desc()).all()
    
    return render_template('upload_photos.html',
                         user=user,
                         booking=booking,
                         client=client,
                         existing_photos=existing_photos)

@main.route('/dashboard/photographer/delete-photo/<int:photo_id>', methods=['POST'])
def delete_photo(photo_id):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    user = User.query.get(session['user_id'])
    if not user or user.role != 'photographer':
        flash('Access denied. Photographers only.')
        return redirect(url_for('main.index'))
    
    photo = Photo.query.get_or_404(photo_id)
    
    if photo.photographer_id != user.id:
        flash('You can only delete photos you have uploaded.')
        return redirect(url_for('main.photographer_dashboard'))
    
    booking_id = photo.booking_id
    
    try:
        if 'supabase.co/storage' in photo.image_url:
            parts = photo.image_url.split('/storage/v1/object/public/')
            if len(parts) == 2:
                bucket_and_path = parts[1].split('/', 1)
                if len(bucket_and_path) == 2:
                    bucket_name = bucket_and_path[0]
                    file_path = bucket_and_path[1]
                    
                    supabase = get_supabase_client()
                    supabase.storage.from_(bucket_name).remove([file_path])
    except Exception as e:
        print(f"Error deleting from storage: {str(e)}")
    
    db.session.delete(photo)
    db.session.commit()
    
    flash('Photo deleted successfully!')
    
    if booking_id:
        return redirect(url_for('main.upload_photos', booking_id=booking_id))
    return redirect(url_for('main.photographer_dashboard'))

@main.route('/auth/register', methods=['POST'])
def register_api():
    data = request.get_json()
    
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'error': 'Email already registered'}), 400
    
    new_user = User(
        username=data['name'],
        email=data['email'],
        password_hash=generate_password_hash(data['password']),
        role=data.get('role', 'client')
    )
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'Registration successful', 'user_id': new_user.id}), 201

@main.route('/auth/login', methods=['POST'])
def login_api():
    data = request.get_json()
    
    user = User.query.filter_by(email=data['email']).first()
    
    if user and check_password_hash(user.password_hash, data['password']):
        session['user_id'] = user.id
        session['user_name'] = user.username
        session['user_role'] = user.role
        
        return jsonify({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'name': user.username,
                'email': user.email,
                'role': user.role
            }
        }), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401

@main.route('/auth/logout', methods=['POST'])
def logout_api():
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200

@main.route('/auth/me', methods=['GET'])
def get_current_user_api():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user = User.query.get(session['user_id'])
    return jsonify({
        'id': user.id,
        'name': user.username,
        'email': user.email,
        'role': user.role
    }), 200

@main.route('/photographers', methods=['GET'])
def get_photographers_api():
    photographers = User.query.filter_by(role='photographer').all()
    
    return jsonify([{
        'id': p.id,
        'name': p.username,
        'bio': p.bio,
        'location': p.location,
        'price_per_hour': float(p.price_per_hour) if p.price_per_hour else None,
        'profile_picture': p.profile_picture,
        'portfolio_url': p.portfolio_url
    } for p in photographers]), 200

@main.route('/photographers/<int:photographer_id>', methods=['GET'])
def get_photographer_api(photographer_id):
    photographer = User.query.get_or_404(photographer_id)
    
    return jsonify({
        'id': photographer.id,
        'name': photographer.username,
        'email': photographer.email,
        'bio': photographer.bio,
        'location': photographer.location,
        'price_per_hour': float(photographer.price_per_hour) if photographer.price_per_hour else None,
        'profile_picture': photographer.profile_picture,
        'portfolio_url': photographer.portfolio_url,
        'phone': photographer.phone
    }), 200

@main.route('/bookings', methods=['GET', 'POST'])
def bookings_api():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    if request.method == 'POST':
        data = request.get_json()
        
        booking_datetime = datetime.fromisoformat(data['booking_date_and_time'])
        
        existing = Booking.query.filter_by(
            photographer_id=data['photographer_id'],
            booking_date_and_time=booking_datetime
        ).first()
        
        if existing:
            return jsonify({'error': 'Time slot already booked'}), 400
        
        new_booking = Booking(
            client_id=session['user_id'],
            photographer_id=data['photographer_id'],
            booking_date_and_time=booking_datetime,
            type=data.get('type', 'session'),
            description=data.get('description', ''),
            status='confirmed'
        )
        db.session.add(new_booking)
        db.session.commit()
        
        return jsonify({
            'message': 'Booking confirmed',
            'booking_id': new_booking.id
        }), 201
    
    user = User.query.get(session['user_id'])
    
    if user.role == 'photographer':
        user_bookings = Booking.query.filter_by(photographer_id=user.id).all()
    else:
        user_bookings = Booking.query.filter_by(client_id=user.id).all()
    
    return jsonify([{
        'id': b.id,
        'client_id': b.client_id,
        'photographer_id': b.photographer_id,
        'booking_date_and_time': b.booking_date_and_time.isoformat(),
        'type': b.type,
        'description': b.description,
        'status': b.status,
        'created_at': b.created_at.isoformat()
    } for b in user_bookings]), 200

@main.route('/bookings/<booking_id>', methods=['DELETE'])
def cancel_booking_api(booking_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    booking = Booking.query.get_or_404(booking_id)
    
    if booking.client_id != session['user_id'] and booking.photographer_id != session['user_id']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(booking)
    db.session.commit()
    
    return jsonify({'message': 'Booking cancelled'}), 200
