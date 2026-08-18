from datetime import datetime
from .extensions import db
from flask_login import UserMixin


class User(UserMixin,db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    is_approved = db.Column(db.Boolean, default=False)
    is_blacklisted = db.Column(db.Boolean, default=False)
    
    bookings = db.relationship("Booking", back_populates="user",cascade="all,delete-orphan",lazy=True)

    
class Trek(db.Model):
    __tablename__ = "treks"

    id = db.Column(db.Integer, primary_key=True)
    trek_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(10), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(15),default="Open", nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    assigned_staff_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=True)
    
    bookings = db.relationship("Booking",back_populates="trek",cascade="all, delete-orphan")
    assigned_staff = db.relationship("User", foreign_keys=[assigned_staff_id])
    
class Booking(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey("treks.id"), nullable=False)
    booking_date = db.Column(db.DateTime,default=datetime.utcnow, nullable=False)
    status = db.Column(db.String(15), default="Booked",nullable=False)
    __table_args__ = (
        db.UniqueConstraint("user_id", "trek_id", name="unique_booking"),
    )
    
    user = db.relationship("User", back_populates="bookings")
    trek = db.relationship("Trek",back_populates = "bookings")