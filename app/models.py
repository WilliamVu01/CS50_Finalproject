# Finalproject/app/models.py
from datetime import datetime
from flask_login import UserMixin
from .extensions import db # Ensure this is correct

# --- User Model ---
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    role = db.Column(db.Enum('admin', 'instructor', 'student', name='user_roles'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships on User model
    # Use string literals for 'Booking' to avoid early resolution issues
    bookings_as_instructor = db.relationship(
        'Booking', # Use string literal for the class name
        foreign_keys='Booking.instructor_id', # String literal is fine here
        back_populates='instructor'
    )
    bookings_as_student = db.relationship(
        'Booking', # Use string literal for the class name
        foreign_keys='Booking.student_id', # String literal is fine here
        back_populates='student'
    )

    def get_id(self):
        return str(self.id)

# --- Training Element Model ---
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

    # Relationship on TrainingElement
    bookings = db.relationship('Booking', back_populates='training_element')

# --- Booking Model ---
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

    # Relationships on Booking
    training_element = db.relationship(
        'TrainingElement', # Use string literal
        back_populates='bookings'
    )
    instructor = db.relationship(
        'User', # Use string literal
        foreign_keys=[instructor_id], # Keep as list of column objects for clarity and correctness
        back_populates='bookings_as_instructor'
    )
    student = db.relationship(
        'User', # Use string literal
        foreign_keys=[student_id], # Keep as list of column objects
        back_populates='bookings_as_student'
    )