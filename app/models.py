from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    bio = db.Column(db.Text)
    location = db.Column(db.String(100))
    price_per_hour = db.Column(db.Numeric(10, 2))
    profile_picture = db.Column(db.String(255))
    portfolio_url = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)


class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(__import__('uuid').uuid4()))
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    photographer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    booking_date_and_time = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Photo(db.Model):
    __tablename__ = 'photos'
    
    id = db.Column(db.Integer, primary_key=True)  # ADD THIS LINE
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    photographer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    booking_id = db.Column(db.String(36), db.ForeignKey('bookings.id'))
    image_url = db.Column(db.String(500), nullable=False)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)


class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)


class PhotographerAvailability(db.Model):
    __tablename__ = 'photographer_availability'
    
    id = db.Column(db.Integer, primary_key=True)
    photographer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    available_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.String(10), nullable=False)
    end_time = db.Column(db.String(10), nullable=False)
    is_available = db.Column(db.Boolean, default=True)



