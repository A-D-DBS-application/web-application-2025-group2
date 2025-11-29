# app/routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from app import db
from app.models import User, Booking, PhotographerAvailability, Photo
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
        photos = Photo.query.filter_by(photographer_id=photographer.id).order_by(Photo.uploaded_at.desc()).limit(2).all()
        photographer_photos[photographer.id] = photos
    
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return render_template('index.html', username=user.username, user=user, photographers=photographers, photographer_photos=photographer_photos)
    
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
            session['user_role'] = user.role
            return redirect(url_for('main.index'))
        else:
            error = "Invalid email or password."

    return render_template('login.html', error=error)

@main.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('You have been logged out successfully.')
    return redirect(url_for('main.index'))

@main.route('/photographers')
def photographers():
    """Browse all photographers"""
    all_photographers = User.query.filter_by(role='photographer').all()
    photographer_data = []
    for photographer in all_photographers:
        photos = Photo.query.filter_by(photographer_id=photographer.id).order_by(Photo.uploaded_at.desc()).limit(6).all()
        photographer_data.append({
            'photographer': photographer,
            'photos': photos
        })
    return render_template('photographers.html', photographers=photographer_data)

@main.route('/photographer/<int:photographer_id>')
def photographer_profile(photographer_id):
    """View photographer profile and book"""
    photographer = User.query.get_or_404(photographer_id)
    if photographer.role != 'photographer':
        flash('Invalid photographer')
        return redirect(url_for('main.index'))
    
    photos = Photo.query.filter_by(photographer_id=photographer.id).order_by(Photo.uploaded_at.desc()).all()
    return render_template('photographer_profile.html', photographer=photographer, photos=photos)

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
        
        # Get the availability slot
        slot = PhotographerAvailability.query.get(slot_id)
        if not slot or slot.photographer_id != int(photographer_id):
            flash('Invalid time slot selected.')
            return redirect(url_for('main.book'))
        
        # Check if slot is still available
        if not slot.is_available:
            flash('This time slot is no longer available.')
            return redirect(url_for('main.book'))
        
        # Combine date and time
        booking_datetime = datetime.combine(
            slot.available_date, 
            datetime.strptime(slot.start_time, '%H:%M').time()
        )
        
        # Create booking
        new_booking = Booking(
            client_id=session['user_id'],
            photographer_id=int(photographer_id),
            booking_date_and_time=booking_datetime,
            type='session',
            description=notes
        )
        db.session.add(new_booking)
        
        # Mark slot as unavailable
        slot.is_available = False
        
        db.session.commit()
        
        # Redirect to confirmation page
        return redirect(url_for('main.booking_confirmation', booking_id=new_booking.id))
    
    # GET request - show form
    # Get all users with photographer role
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
    
    # Get photographer name from User table
    photographer = User.query.get(booking.photographer_id)
    photographer_name = photographer.name if photographer else 'Unknown'
    
    return render_template('booking_confirmation.html', 
                         booking=booking,
                         photographer_name=photographer_name)

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
    
    # Get all users with photographer role
    photographers = User.query.filter_by(role='photographer').all()
    return render_template('add_availability.html', photographers=photographers)

@main.route('/bookings')
def bookings():
    if 'user_id' not in session:
        flash('Please log in to view bookings.')
        return redirect(url_for('main.login'))
    
    user = User.query.get(session['user_id'])
    
    # If user is a photographer, show their bookings
    if user.role == 'photographer':
        user_bookings = Booking.query.filter_by(photographer_id=user.id).order_by(Booking.booking_date_and_time.desc()).all()
    # If user is a client, show their bookings
    else:
        user_bookings = Booking.query.filter_by(client_id=user.id).order_by(Booking.booking_date_and_time.desc()).all()
    
    return render_template('bookings.html', bookings=user_bookings, user=user)


@main.route('/bookings/<booking_id>')
def booking_detail(booking_id):
    if 'user_id' not in session:
        flash('Please log in to view booking details.')
        return redirect(url_for('main.login'))
    
    booking = Booking.query.get_or_404(booking_id)
    
    # Security: ensure user can only view their own bookings
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
    
    # Only photographer or client can update
    if booking.client_id != session['user_id'] and booking.photographer_id != session['user_id']:
        flash('You do not have permission to update this booking.')
        return redirect(url_for('main.bookings'))
    
    # Update booking details
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

@main.route('/dashboard/photographer')
def photographer_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    user = User.query.get(session['user_id'])
    if not user or user.role != 'photographer':
        flash('Access denied. Photographers only.')
        return redirect(url_for('main.index'))
    
    # Get bookings from clients (where this user is the photographer)
    bookings = Booking.query.filter_by(photographer_id=user.id).order_by(Booking.booking_date_and_time.desc()).all()
    
    # Attach client objects and photo counts to bookings
    for booking in bookings:
        booking.client = User.query.get(booking.client_id)
        booking.photo_count = Photo.query.filter_by(booking_id=booking.id).count()
    
    return render_template('photographer_dashboard_new.html',
                         user=user,
                         bookings=bookings)

@main.route('/dashboard/photographer/complete-booking/<booking_id>', methods=['POST'])
def complete_booking(booking_id):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    user = User.query.get(session['user_id'])
    if not user or user.role != 'photographer':
        flash('Access denied.')
        return redirect(url_for('main.index'))
    
    booking = Booking.query.get_or_404(booking_id)
    
    # Security check: only the photographer can complete their booking
    if booking.photographer_id != user.id:
        flash('You can only complete your own bookings.')
        return redirect(url_for('main.photographer_dashboard'))
    
    booking.status = 'completed'
    db.session.commit()
    
    flash('Booking marked as completed.')
    return redirect(url_for('main.photographer_dashboard'))
    
    # Get photos OF this photographer (as a client)
    photos_as_client = Photo.query.filter_by(user_id=user.id).order_by(Photo.uploaded_at.desc()).all()
    
    # Group photos as client by photographer
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
    
    # Create availability slot
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
    
    # Get the slot
    slot = PhotographerAvailability.query.get_or_404(slot_id)
    
    # Security check: ensure the photographer owns this slot
    if slot.photographer_id != user.id:
        flash('You can only delete your own availability slots.')
        return redirect(url_for('main.photographer_dashboard'))
    
    # Check if slot is already booked
    if not slot.is_available:
        flash('Cannot delete a slot that has already been booked.')
        return redirect(url_for('main.photographer_dashboard'))
    
    # Delete the slot
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
    
    # Get bookings with photographer information (eager loading)
    bookings = db.session.query(Booking).join(User, Booking.photographer_id == User.id).filter(
        Booking.client_id == user.id
    ).order_by(Booking.booking_date_and_time.desc()).all()
    
    # Attach photographer objects and photo counts to bookings and prepare for JSON serialization
    bookings_list = []
    for booking in bookings:
        booking.photographer = User.query.get(booking.photographer_id)
        booking.photo_count = Photo.query.filter_by(booking_id=booking.id).count()
        bookings_list.append({
            'id': booking.id,
            'booking_date_and_time': booking.booking_date_and_time.isoformat() if booking.booking_date_and_time else None,
            'type': booking.type,
            'status': booking.status,
            'photographer_name': booking.photographer.name if booking.photographer else 'Unknown'
        })
    
    # Get photos of this client, grouped by photographer
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
                         bookings_json=bookings_list,
                         photos_by_photographer=photos_by_photographer)

@main.route('/dashboard/photographer/upload-photos/<booking_id>', methods=['GET', 'POST'])
def upload_photos(booking_id):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    user = User.query.get(session['user_id'])
    if not user or user.role != 'photographer':
        flash('Access denied. Photographers only.')
        return redirect(url_for('main.index'))
    
    # Get the booking
    booking = Booking.query.get_or_404(booking_id)
    
    # Security check: ensure photographer owns this booking
    if booking.photographer_id != user.id:
        flash('You can only upload photos for your own bookings.')
        return redirect(url_for('main.photographer_dashboard'))
    
    # Get client info
    booking.client = User.query.get(booking.client_id)
    
    # Get existing photos for this booking
    photos = Photo.query.filter_by(booking_id=booking_id).order_by(Photo.uploaded_at.desc()).all()
    
    if request.method == 'POST':
        # Check if files were uploaded
        if 'photos' not in request.files:
            flash('No files selected.')
            return redirect(url_for('main.upload_photos', booking_id=booking_id))
        
        files = request.files.getlist('photos')
        
        if not files or files[0].filename == '':
            flash('No files selected.')
            return redirect(url_for('main.upload_photos', booking_id=booking_id))
        
        # Validate and upload files
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
        uploaded_count = 0
        
        for file in files:
            try:
                # Generate unique filename
                file_ext = file.filename.rsplit('.', 1)[1].lower()
                unique_filename = f"{uuid.uuid4()}.{file_ext}"
                file_path = f"bookings/{booking_id}/{unique_filename}"
                
                # Upload to Supabase Storage
                supabase = get_supabase_client()
                file_content = file.read()
                
                supabase.storage.from_('photos').upload(
                    file_path,
                    file_content,
                    {'content-type': file.content_type}
                )
                
                # Get public URL
                photo_url = supabase.storage.from_('photos').get_public_url(file_path)
                
                # Create photo record with storage URL
                new_photo = Photo(
                    user_id=booking.client_id,
                    photographer_id=user.id,
                    booking_id=booking.id,
                    image_url=photo_url,
                    title=file.filename
                )
                db.session.add(new_photo)
                uploaded_count += 1
                
            except Exception as e:
                flash(f'Error uploading {file.filename}: {str(e)}')
                continue
        
        if uploaded_count > 0:
            db.session.commit()
            flash(f'{uploaded_count} photo(s) uploaded successfully!')
        else:
            flash('No photos were uploaded.')
        
        return redirect(url_for('main.upload_photos', booking_id=booking_id))
    
    return render_template('upload_photos_new.html',
                         user=user,
                         booking=booking,
                         photos=photos)

@main.route('/dashboard/photographer/delete-photo/<int:photo_id>', methods=['POST'])
def delete_photo(photo_id):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    user = User.query.get(session['user_id'])
    if not user or user.role != 'photographer':
        flash('Access denied. Photographers only.')
        return redirect(url_for('main.index'))
    
    # Get the photo
    photo = Photo.query.get_or_404(photo_id)
    
    # Security check: ensure photographer owns this photo
    if photo.photographer_id != user.id:
        flash('You can only delete photos you have uploaded.')
        return redirect(url_for('main.photographer_dashboard'))
    
    # Store booking_id for redirect
    booking_id = photo.booking_id
    
    # Delete from Supabase Storage if it's a storage URL
    try:
        if 'supabase.co/storage' in photo.image_url:
            # Extract file path from URL
            # URL format: https://PROJECT.supabase.co/storage/v1/object/public/BUCKET/PATH
            parts = photo.image_url.split('/storage/v1/object/public/')
            if len(parts) == 2:
                bucket_and_path = parts[1].split('/', 1)
                if len(bucket_and_path) == 2:
                    bucket_name = bucket_and_path[0]
                    file_path = bucket_and_path[1]
                    
                    supabase = get_supabase_client()
                    supabase.storage.from_(bucket_name).remove([file_path])
    except Exception as e:
        # If deletion from storage fails, continue with database deletion
        print(f"Error deleting from storage: {str(e)}")
    
    # Delete from database
    db.session.delete(photo)
    db.session.commit()
    
    flash('Photo deleted successfully!')
    
    # Redirect back to upload page if booking_id exists, otherwise to dashboard
    if booking_id:
        return redirect(url_for('main.upload_photos', booking_id=booking_id))
    return redirect(url_for('main.photographer_dashboard'))

@main.route('/booking/photos/<booking_id>')
def view_booking_photos(booking_id):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        return redirect(url_for('main.login'))
    
    # Get the booking
    booking = Booking.query.get_or_404(booking_id)
    
    # Security check: only the client can view their photos
    if booking.client_id != user.id:
        flash('You can only view photos from your own bookings.')
        return redirect(url_for('main.client_dashboard'))
    
    # Get photographer info
    booking.photographer = User.query.get(booking.photographer_id)
    
    # Get photos for this booking
    photos = Photo.query.filter_by(booking_id=booking_id).order_by(Photo.uploaded_at.desc()).all()
    
    return render_template('view_booking_photos.html',
                         user=user,
                         booking=booking,
                         photos=photos)

@main.route('/booking/cancel/<booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        return redirect(url_for('main.login'))
    
    # Get the booking
    booking = Booking.query.get_or_404(booking_id)
    
    # Security check: only the client can cancel their booking
    if booking.client_id != user.id:
        flash('You can only cancel your own bookings.')
        return redirect(url_for('main.client_dashboard'))
    
    # Free up the availability slot
    if booking.booking_date_and_time:
        # Find the corresponding availability slot
        slot = PhotographerAvailability.query.filter_by(
            photographer_id=booking.photographer_id,
            available_date=booking.booking_date_and_time.date(),
            is_available=False
        ).first()
        
        if slot:
            slot.is_available = True
    
    # Delete the booking
    db.session.delete(booking)
    db.session.commit()
    
    flash('Booking cancelled successfully!')
    return redirect(url_for('main.client_dashboard'))

@main.route('/booking/delete/<booking_id>', methods=['POST'])
def delete_booking(booking_id):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        return redirect(url_for('main.login'))
    
    # Get the booking
    booking = Booking.query.get_or_404(booking_id)
    
    # Security check: client can delete their own bookings, photographer can delete their client bookings
    if booking.client_id != user.id and booking.photographer_id != user.id:
        flash('You can only delete your own bookings.')
        if user.role == 'photographer':
            return redirect(url_for('main.photographer_dashboard'))
        return redirect(url_for('main.client_dashboard'))
    
    # Only allow deleting completed or cancelled bookings
    if booking.status not in ['completed', 'cancelled']:
        flash('You can only delete completed or cancelled bookings.')
        if user.role == 'photographer':
            return redirect(url_for('main.photographer_dashboard'))
        return redirect(url_for('main.client_dashboard'))
    
    # Delete associated photos first
    Photo.query.filter_by(booking_id=booking_id).delete()
    
    # Delete the booking
    db.session.delete(booking)
    db.session.commit()
    
    flash('Booking and associated photos deleted successfully!')
    
    if user.role == 'photographer':
        return redirect(url_for('main.photographer_dashboard'))
    return redirect(url_for('main.client_dashboard'))
