from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


class Category(db.Model):
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Category {self.name}>'



class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    client_id = db.Column(db.Integer, nullable=True)  # Changed from user_id, int4 type
    photographer_id = db.Column(db.Integer, nullable=True)  # Changed to nullable
    booking_date = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(120), nullable=True)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True)

    # Remove the relationship for now since client_id is int4, not a foreign key to clients table
    
    def __repr__(self):
        return f'<Booking {self.id}>'


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
    __tablename__ = 'feedback'
    id = db.Column(pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    booking_id = db.Column(pg.UUID(as_uuid=True), db.ForeignKey('bookings.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    booking = db.relationship('Booking', backref=db.backref('feedbacks', lazy=True))

    def __repr__(self):
        return f'<Feedback {self.id}>'


class Notification(db.Model):
    notification_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('notifications', lazy=True))

    def __repr__(self):
        return f'<Notification {self.notification_id}>'



