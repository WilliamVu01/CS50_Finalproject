# Finalproject/app/models.py
from datetime import datetime
from flask_login import UserMixin
from .extensions import db, bcrypt

# --- User Model ---
# User (id, email, password_hash, first_name, last_name, role: admin/instructor/student, created_at, updated_at)
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    role = db.Column(db.Enum('admin', 'instructor', 'student', name='user_roles'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

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
    created_bookings = db.relationship(
        'Booking',
        foreign_keys='Booking.created_by_user_id',
        back_populates='created_by'
    )

    def get_id(self):
        # Flask-Login expects the ID returned by get_id() to be a string
        return str(self.id)
    # Methods for password handling - critical for Flask-Login
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

# --- Training Element Model ---
# TrainingElement (id, name, description, duration_minutes, session_type, material_link, created_at, updated_at)
class TrainingElement(db.Model):
    __tablename__ = 'training_elements'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    duration_minutes = db.Column(db.Integer, nullable=False)
    session_type = db.Column(db.Enum('classroom', 'hands_on', 'e_learning', 'assessment', name='session_types'), nullable=False)
    material_link = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    # Relationship on TrainingElement
    bookings = db.relationship('Booking', back_populates='training_element')

# --- Booking Model ---
# Booking (id, training_element_id, start_time, end_time, instructor_id, student_id, created_at, updated_at)
class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    training_element_id = db.Column(db.Integer, db.ForeignKey('training_elements.id'), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum('pending', 'confirmed', 'completed', 'cancelled', name='booking_statuses'), nullable=False, default='pending')
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    notes = db.Column(db.Text, nullable=True)

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
    # New: Relationship for the user who created this booking
    created_by = db.relationship(
        'User',
        foreign_keys=[created_by_user_id],
        back_populates='created_bookings'
    )