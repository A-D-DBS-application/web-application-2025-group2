from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from app import db
from app.models import User, Booking, Photo, PhotographerAvailability, Album, Rating
from app.constants import BOOKING_STATUS_COMPLETED
from datetime import datetime
import uuid
from werkzeug.utils import secure_filename
from app.utils.decorators import login_required, photographer_required
from app.utils.helpers import get_current_user, get_supabase_client

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/admin/add-availability', methods=['GET', 'POST'])
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

@dashboard_bp.route('/dashboard/photographer')
@photographer_required
def photographer_dashboard():
    user = get_current_user()
    
    # Get bookings from clients (where this user is the photographer)
    bookings = Booking.query.filter_by(photographer_id=user.id).order_by(Booking.booking_date_and_time.desc()).all()
    
    # Attach client objects and photo counts to bookings
    for booking in bookings:
        booking.client = User.query.get(booking.client_id)
        booking.photo_count = Photo.query.filter_by(booking_id=booking.id).count()
    
    return render_template('photographer_dashboard_new.html',
                         user=user,
                         bookings=bookings)

@dashboard_bp.route('/dashboard/photographer/complete-booking/<booking_id>', methods=['POST'])
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
        return redirect(url_for('dashboard.photographer_dashboard'))
    
    booking.status = 'completed'
    db.session.commit()
    
    flash('Booking marked as completed.')
    return redirect(url_for('dashboard.photographer_dashboard'))

@dashboard_bp.route('/photographer/add-availability', methods=['POST'])
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
        return redirect(url_for('dashboard.photographer_dashboard'))
    
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
    return redirect(url_for('dashboard.photographer_dashboard'))

@dashboard_bp.route('/dashboard/photographer/delete-slot/<int:slot_id>', methods=['POST'])
@photographer_required
def delete_slot(slot_id):
    user = get_current_user()
    
    # Get the slot
    slot = PhotographerAvailability.query.get_or_404(slot_id)
    
    # Security check: ensure the photographer owns this slot
    if slot.photographer_id != user.id:
        flash('You can only delete your own availability slots.')
        return redirect(url_for('dashboard.photographer_dashboard'))
    
    # Check if slot is already booked
    if not slot.is_available:
        flash('Cannot delete a slot that has already been booked.')
        return redirect(url_for('dashboard.photographer_dashboard'))
    
    # Delete the slot
    db.session.delete(slot)
    db.session.commit()
    
    flash('Availability slot deleted successfully!')
    return redirect(url_for('dashboard.photographer_dashboard'))

@dashboard_bp.route('/dashboard/client')
@login_required
def client_dashboard():
    user = get_current_user()
    
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

@dashboard_bp.route('/portfolio/manage')
def manage_portfolio():
    """Photographer's portfolio management interface"""
    if 'user_id' not in session:
        flash('Please login to access this page', 'danger')
        return redirect(url_for('main.login'))
    
    user = User.query.get(session['user_id'])
    if user.role != 'photographer':
        flash('Only photographers can manage portfolios', 'danger')
        return redirect(url_for('main.index'))
    
    albums = Album.query.filter_by(photographer_id=user.id).order_by(Album.created_at.desc()).all()
    return render_template('manage_portfolio.html', user=user, albums=albums)


@dashboard_bp.route('/portfolio/album/create', methods=['POST'])
def create_album():
    """Create a new album/category"""
    if 'user_id' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('main.login'))
    
    user = User.query.get(session['user_id'])
    if user.role != 'photographer':
        flash('Only photographers can create albums', 'danger')
        return redirect(url_for('main.index'))
    
    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()
    
    if not name:
        flash('Album name is required', 'danger')
        return redirect(url_for('dashboard.manage_portfolio'))
    
    new_album = Album(
        photographer_id=user.id,
        name=name,
        description=description if description else None
    )
    
    db.session.add(new_album)
    db.session.commit()
    
    flash(f'Album "{name}" created! Now add your photos.', 'success')
    # Redirect directly to upload page for the new album
    return redirect(url_for('dashboard.upload_to_album', album_id=new_album.id))


@dashboard_bp.route('/portfolio/album/<int:album_id>/upload', methods=['GET', 'POST'])
def upload_to_album(album_id):
    """Upload photos to a specific album"""
    if 'user_id' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('main.login'))
    
    album = Album.query.get_or_404(album_id)
    
    # Check if user is the album owner
    if album.photographer_id != session['user_id']:
        flash('You can only upload to your own albums', 'danger')
        return redirect(url_for('dashboard.manage_portfolio'))
    
    if request.method == 'POST':
        if 'photo_file' not in request.files:
            flash('No file selected', 'danger')
            return redirect(request.url)
        
        file = request.files['photo_file']
        if file.filename == '':
            flash('No file selected', 'danger')
            return redirect(request.url)
        
        # Validate file extension
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
        if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            flash('Invalid file type. Please upload an image file (png, jpg, jpeg, gif, webp)', 'danger')
            return redirect(request.url)
        
        try:
            # Generate unique filename
            original_filename = secure_filename(file.filename)
            file_ext = original_filename.rsplit('.', 1)[1].lower()
            unique_filename = f"{uuid.uuid4()}.{file_ext}"
            
            # Upload to Supabase Storage
            supabase = get_supabase_client()
            bucket_name = current_app.config['SUPABASE_STORAGE_BUCKET']
            
            # Path: albums/{album_id}/{unique_filename}
            storage_path = f"albums/{album_id}/{unique_filename}"
            
            # Read file data
            file_data = file.read()
            
            # Upload to Supabase
            response = supabase.storage.from_(bucket_name).upload(
                path=storage_path,
                file=file_data,
                file_options={"content-type": file.content_type}
            )
            
            # Get public URL
            public_url = supabase.storage.from_(bucket_name).get_public_url(storage_path)
            
            # Create Photo record
            title = request.form.get('title', '').strip()
            new_photo = Photo(
                user_id=session['user_id'],
                photographer_id=session['user_id'],
                album_id=album_id,
                image_url=public_url,
                title=title if title else None
            )
            
            db.session.add(new_photo)
            db.session.commit()
            
            flash('Photo uploaded successfully!', 'success')
            return redirect(url_for('dashboard.upload_to_album', album_id=album_id))
            
        except Exception as e:
            flash(f'Error uploading photo: {str(e)}', 'danger')
            return redirect(request.url)
    
    return render_template('upload_to_album.html', album=album)


@dashboard_bp.route('/portfolio/album/<int:album_id>/delete', methods=['POST'])
def delete_album(album_id):
    """Delete an album and all its photos"""
    if 'user_id' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('main.login'))
    
    album = Album.query.get_or_404(album_id)
    
    # Check if user is the album owner
    if album.photographer_id != session['user_id']:
        flash('You can only delete your own albums', 'danger')
        return redirect(url_for('dashboard.manage_portfolio'))
    
    try:
        supabase = get_supabase_client()
        bucket_name = current_app.config['SUPABASE_STORAGE_BUCKET']
        
        # Delete all photos from storage and database
        for photo in album.photos:
            # Extract file path from URL
            if photo.image_url:
                url_parts = photo.image_url.split(f'{bucket_name}/')
                if len(url_parts) > 1:
                    file_path = url_parts[1]
                    try:
                        supabase.storage.from_(bucket_name).remove([file_path])
                    except:
                        pass  # Continue even if storage deletion fails
            
            db.session.delete(photo)
        
        # Delete album
        album_name = album.name
        db.session.delete(album)
        db.session.commit()
        
        flash(f'Album "{album_name}" and all its photos deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting album: {str(e)}', 'danger')
    
    return redirect(url_for('dashboard.manage_portfolio'))

@dashboard_bp.route('/dashboard/photographer/upload-photos/<booking_id>', methods=['GET', 'POST'])
def upload_photos(booking_id):
    print(f"\n🔍 Route called - Method: {request.method}, Booking: {booking_id}")
    
    if 'user_id' not in session:
        print("❌ FAILED: No user_id in session")
        return redirect(url_for('main.login'))
    
    print(f"✅ User in session: {session['user_id']}")
    
    user = User.query.get(session['user_id'])
    if not user:
        print("❌ FAILED: User not found in database")
        return redirect(url_for('main.login'))
    
    print(f"✅ User found: {user.name}, Role: {user.role}")
    
    if user.role != 'photographer':
        print(f"❌ FAILED: User is not photographer (role: {user.role})")
        flash('Access denied.')
        return redirect(url_for('main.index'))
    
    print(f"✅ User is photographer")
    
    booking = Booking.query.get(booking_id)
    if not booking:
        print(f"❌ FAILED: Booking {booking_id} not found")
        flash('Booking not found.')
        return redirect(url_for('dashboard.photographer_dashboard'))
    
    print(f"✅ Booking found: {booking.id}")
    print(f"   Photographer ID on booking: {booking.photographer_id}")
    print(f"   Current user ID: {user.id}")
    
    if booking.photographer_id != user.id:
        print(f"❌ FAILED: Booking photographer ({booking.photographer_id}) != current user ({user.id})")
        flash('Booking not found.')
        return redirect(url_for('dashboard.photographer_dashboard'))
    
    print(f"✅ Booking belongs to photographer")
    
    if request.method == 'POST':
        print("\n" + "="*70)
        print("POST REQUEST - UPLOAD STARTING")
        print("="*70)
        
        files = request.files.getlist('photos')
        print(f"Files received: {len(files)}")
        
        if not files or files[0].filename == '':
            print("❌ FAILED: No files or empty filename")
            flash('No files selected.')
            return redirect(request.url)
        
        print("✅ File validation passed")
        
        try:
            supabase = get_supabase_client()
            print(f"✅ Supabase client created")
            
            uploaded_count = 0
            for file in files:
                if file and file.filename:
                    print(f"\n--- Processing: {file.filename} ---")
                    
                    file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else 'jpg'
                    unique_filename = f"{uuid.uuid4()}.{file_ext}"
                    print(f"  Unique filename: {unique_filename}")
                    
                    file_content = file.read()
                    print(f"  File size: {len(file_content)} bytes")
                    
                    print("  Uploading to Supabase...")
                    response = supabase.storage.from_('photos').upload(
                        path=unique_filename,
                        file=file_content,
                        file_options={"content-type": file.content_type}
                    )
                    print(f"  ✅ Uploaded to Supabase: {response}")
                    
                    photo_url = supabase.storage.from_('photos').get_public_url(unique_filename)
                    print(f"  ✅ Photo URL: {photo_url}")
                    
                    new_photo = Photo(
                        user_id=booking.client_id,
                        photographer_id=user.id,
                        booking_id=booking.id,
                        image_url=photo_url,
                        title=file.filename,
                        category_id=None
                    )
                    
                    db.session.add(new_photo)
                    print(f"  ✅ Added to DB session")
                    uploaded_count += 1
            
            db.session.commit()
            print(f"\n✅ COMMIT SUCCESSFUL - {uploaded_count} photos uploaded to Supabase")
            
            flash(f'Successfully uploaded {uploaded_count} photo(s)!')
            return redirect(url_for('dashboard.upload_photos', booking_id=booking_id))
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
            flash(f'Error uploading photos: {str(e)}')
            return redirect(request.url)
    
    photos = Photo.query.filter_by(booking_id=booking_id).all()
    return render_template('upload_photos_new.html', booking=booking, photos=photos)

@dashboard_bp.route('/dashboard/photographer/delete-photo/<int:photo_id>', methods=['POST'])
@photographer_required
def delete_photo(photo_id):
    user = get_current_user()
    
    # Get the photo
    photo = Photo.query.get_or_404(photo_id)
    
    # Security check: ensure photographer owns this photo
    if photo.photographer_id != user.id:
        flash('You can only delete photos you have uploaded.')
        return redirect(url_for('dashboard.photographer_dashboard'))
    
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
        return redirect(url_for('dashboard.upload_photos', booking_id=booking_id))
    return redirect(url_for('dashboard.photographer_dashboard'))

@dashboard_bp.route('/booking/photos/<booking_id>')
@login_required
def view_booking_photos(booking_id):
    user = get_current_user()
    
    # Get the booking
    booking = Booking.query.get_or_404(booking_id)
    
    # Security check: only the client can view their photos
    if booking.client_id != user.id:
        flash('You can only view photos from your own bookings.')
        return redirect(url_for('dashboard.client_dashboard'))
    
    # Get photographer info
    booking.photographer = User.query.get(booking.photographer_id)
    
    # Get photos for this booking
    photos = Photo.query.filter_by(booking_id=booking_id).order_by(Photo.uploaded_at.desc()).all()
    
    return render_template('view_booking_photos.html',
                         user=user,
                         booking=booking,
                         photos=photos)

@dashboard_bp.route('/booking/<booking_id>/rate', methods=['GET', 'POST'])
@login_required
def rate_booking(booking_id):
    """Allow client to rate a completed booking"""
    user = get_current_user()
    
    booking = Booking.query.get_or_404(booking_id)
    
    # Security: only client can rate
    if booking.client_id != user.id:
        flash('You can only rate your own bookings.', 'danger')
        return redirect(url_for('dashboard.client_dashboard'))
    
    # Check if booking is completed
    if booking.status != BOOKING_STATUS_COMPLETED:
        flash('You can only rate completed bookings.', 'warning')
        return redirect(url_for('dashboard.client_dashboard'))
    
    # Check if already rated
    existing_rating = Rating.query.filter_by(booking_id=booking_id).first()
    
    if request.method == 'POST':
        if existing_rating:
            flash('You have already rated this booking.', 'warning')
            return redirect(url_for('dashboard.client_dashboard'))
        
        rating_value = request.form.get('rating', type=int)
        review_text = request.form.get('review', '').strip()
        
        if not rating_value or rating_value < 1 or rating_value > 5:
            flash('Please select a rating between 1 and 5 stars.', 'danger')
            return redirect(request.url)
        
        # Create rating
        new_rating = Rating(
            booking_id=booking.id,
            client_id=user.id,
            photographer_id=booking.photographer_id,
            rating=rating_value,
            review=review_text if review_text else None
        )
        
        db.session.add(new_rating)
        db.session.commit()
        
        flash('Thank you for your review!', 'success')
        return redirect(url_for('dashboard.client_dashboard'))
    
    # GET request - show rating form
    photographer = User.query.get(booking.photographer_id)
    return render_template('rate_booking.html',
                         booking=booking,
                         photographer=photographer,
                         existing_rating=existing_rating)

@dashboard_bp.route('/booking/cancel/<booking_id>', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    user = get_current_user()
    
    # Get the booking
    booking = Booking.query.get_or_404(booking_id)
    
    # Security check: only the client can cancel their booking
    if booking.client_id != user.id:
        flash('You can only cancel your own bookings.')
        return redirect(url_for('dashboard.client_dashboard'))
    
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
    return redirect(url_for('dashboard.client_dashboard'))

@dashboard_bp.route('/booking/delete/<booking_id>', methods=['POST'])
@login_required
def delete_booking(booking_id):
    user = get_current_user()
    
    # Get the booking
    booking = Booking.query.get_or_404(booking_id)
    
    # Security check: client can delete their own bookings, photographer can delete their client bookings
    if booking.client_id != user.id and booking.photographer_id != user.id:
        flash('You can only delete your own bookings.')
        if user.role == 'photographer':
            return redirect(url_for('dashboard.photographer_dashboard'))
        return redirect(url_for('dashboard.client_dashboard'))
    
    # Only allow deleting completed or cancelled bookings
    if booking.status not in ['completed', 'cancelled']:
        flash('You can only delete completed or cancelled bookings.')
        if user.role == 'photographer':
            return redirect(url_for('dashboard.photographer_dashboard'))
        return redirect(url_for('dashboard.client_dashboard'))
    
    # Delete associated photos first
    Photo.query.filter_by(booking_id=booking_id).delete()
    
    # Delete the booking
    db.session.delete(booking)
    db.session.commit()
    
    flash('Booking and associated photos deleted successfully!')
    
    if user.role == 'photographer':
        return redirect(url_for('dashboard.photographer_dashboard'))
    return redirect(url_for('dashboard.client_dashboard'))

