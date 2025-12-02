from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)


class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    photographer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    booking_date_and_time = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    client = db.relationship('User', foreign_keys=[client_id], backref='client_bookings')
    photographer = db.relationship('User', foreign_keys=[photographer_id], backref='photographer_bookings')


class Photo(db.Model):
    __tablename__ = 'photo'
    
    # Match the actual database column names
    photo_id = db.Column('photo_id', db.Integer, primary_key=True)  # Primary key is 'photo_id'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    image_url = db.Column(db.Text, nullable=False)
    uploaded_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    photographer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    booking_id = db.Column(UUID(as_uuid=True), db.ForeignKey('bookings.id'), nullable=True)
    title = db.Column(db.String, nullable=True)
    
    # Make 'id' an alias for 'photo_id' so your code still works
    @property
    def id(self):
        return self.photo_id


class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)


class PhotographerAvailability(db.Model):
    __tablename__ = 'photographer_availability'
    
    id = db.Column(db.Integer, primary_key=True)
    photographer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    available_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.String(10), nullable=False)
    end_time = db.Column(db.String(10), nullable=False)
    is_available = db.Column(db.Boolean, default=True)



