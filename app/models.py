from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
    
# ...existing code...
class Category(db.Model):
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Category {self.name}>'


class Client(db.Model):
    clientid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Client {self.clientid} {self.email}>'


class Photographer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Photographer {self.id}>'


class Booking(db.Model):
    booking_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.clientid'), nullable=False)
    photographer_id = db.Column(db.Integer, db.ForeignKey('photographer.id'), nullable=False)
    booking_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    client = db.relationship('Client', backref=db.backref('bookings', lazy=True))
    photographer = db.relationship('Photographer', backref=db.backref('bookings', lazy=True))

    def __repr__(self):
        return f'<Booking {self.booking_id}>'


class Photo(db.Model):
    photo_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'), nullable=True)
    image_url = db.Column(db.String(1024), nullable=False)
    uploaded_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('photos', lazy=True))
    category = db.relationship('Category', backref=db.backref('photos', lazy=True))

    def __repr__(self):
        return f'<Photo {self.photo_id}>'


class Tag(db.Model):
    tag_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<Tag {self.name}>'


class PhotoTag(db.Model):
    photo_id = db.Column(db.Integer, db.ForeignKey('photo.photo_id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.tag_id'), primary_key=True)

    photo = db.relationship('Photo', backref=db.backref('photo_tags', lazy=True))
    tag = db.relationship('Tag', backref=db.backref('photo_tags', lazy=True))

    def __repr__(self):
        return f'<PhotoTag photo={self.photo_id} tag={self.tag_id}>'


class Feedback(db.Model):
    feedback_id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.booking_id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    booking = db.relationship('Booking', backref=db.backref('feedbacks', lazy=True))

    def __repr__(self):
        return f'<Feedback {self.feedback_id}>'


class Notification(db.Model):
    notification_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('notifications', lazy=True))

    def __repr__(self):
        return f'<Notification {self.notification_id}>'


class KVStore(db.Model):
    key = db.Column(db.String(255), primary_key=True)
    value = db.Column(db.JSON, nullable=True)

    def __repr__(self):
        return f'<KVStore {self.key}>'
# ...existing code...


class...