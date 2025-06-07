from app import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


# --- User Model ---
# User (id, email, password_hash, first_name, last_name, role: admin/instructor/student, created_at, updated_at)
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    role = db.Column(db.Enum('admin', 'instructor', 'student', name='user_roles'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    # bookings_as_instructor is a list of class that a instructor teach
    # the instructor's list of classes to automatically include that class session
    bookings_as_instructor = db.relationship('Booking', foreign_keys='Booking.instructor_id', back_populates='instructor')
     # bookings_as_student is a list of class that a student enroll
    bookings_as_student = db.relationship('Booking', foreign_keys='Booking.student_id', back_populates='student')

# --- Training Element Model ---
# TrainingElement (id, name, description, duration_minutes, session_type, material_link, created_at, updated_at)
class TrainingElement(db.Model):
    __tablename__ = 'training_elements'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    duration_minutes = db.Column(db.Integer)
    session_type = db.Column(db.String(50))
    material_link = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    # declare relationship with "bookings" table 
    bookings = db.relationship('Booking', back_populates='training_element')

# --- Booking Model ---
# Booking (id, training_element_id, start_time, end_time, instructor_id, student_id, created_at, updated_at)
class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    training_element_id = db.Column(db.Integer, db.ForeignKey('training_elements.id'))
    instructor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    # Relationship with "users" table
    training_element = db.relationship('TrainingElement', back_populates='bookings')
    instructor = db.relationship('User', foreign_keys=[instructor_id], back_populates='bookings_as_instructor')
    student = db.relationship('User', foreign_keys=[student_id], back_populates='bookings_as_student')
