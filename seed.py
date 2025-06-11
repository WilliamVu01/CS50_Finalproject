# Finalproject/seed.py

from app import db, create_app
from app.models import User, TrainingElement, Booking
from app.extensions import bcrypt # Import bcrypt for password hashing
from datetime import datetime, timedelta
# Removed: from werkzeug.security import generate_password_hash (not needed as we use bcrypt directly)

def seed():
    print("--- Starting database seeding ---")
    # Drop and recreate all tables
    print("Dropping all tables...")
    db.drop_all()
    print("Creating all tables...")
    db.create_all()

    # Create users
    print("Creating users...")
    admin = User(
        email='admin@example.com',
        # Use bcrypt.generate_password_hash and decode to string
        password_hash=bcrypt.generate_password_hash('admin123').decode('utf-8'),
        first_name='Admin',
        last_name='William',
        role='admin'
    )

    instructor = User(
        email='instructor@example.com',
        password_hash=bcrypt.generate_password_hash('teachpass').decode('utf-8'),
        first_name='Jimmy',
        last_name='Le',
        role='instructor'
    )

    student = User(
        email='student@example.com',
        password_hash=bcrypt.generate_password_hash('studentpass').decode('utf-8'),
        first_name='Brian',
        last_name='Nguyen',
        role='student'
    )

    db.session.add_all([admin, instructor, student])
    db.session.commit()
    print("Users created.")

    # Create training elements
    print("Creating training elements...")
    te1 = TrainingElement(
        name='Mould TPM',
        description='Mould cleaning',
        duration_minutes=60,
        session_type='classroom', # Ensure this is one of your allowed enum values
        material_link='https://example.com/mould-tpm'
    )

    te2 = TrainingElement(
        name='Machine TPM',
        description='Machine cleaning and practice.',
        duration_minutes=45,
        session_type='hands_on', # Ensure this is one of your allowed enum values
        material_link='https://example.com/machine-tpm'
    )

    db.session.add_all([te1, te2])
    db.session.commit()
    print("Training elements created.")

    # Create bookings
    print("Creating bookings...")
    now = datetime.utcnow() # Use utcnow() for consistency with default=db.func.now()
    booking1 = Booking(
        training_element_id=te1.id,
        instructor_id=instructor.id,
        student_id=student.id,
        start_time=now + timedelta(days=2, hours=9), # Added specific time for better scheduling
        end_time=now + timedelta(days=2, hours=9, minutes=te1.duration_minutes),
        # Crucial: Assign who created the booking
        created_by_user_id=admin.id,
        status='confirmed' # Example: explicitly set status, defaults to 'pending'
    )

    booking2 = Booking(
        training_element_id=te2.id,
        instructor_id=instructor.id,
        student_id=student.id,
        start_time=now + timedelta(days=3, hours=10), # Added specific time
        end_time=now + timedelta(days=3, hours=10, minutes=te2.duration_minutes),
        # Crucial: Assign who created the booking
        created_by_user_id=admin.id,
        status='pending', # Example: use default or explicitly set
        notes='Follow up on previous session.' # Example: added notes
    )

    db.session.add_all([booking1, booking2])
    db.session.commit()
    print("Bookings created.")

    print("✅ Seeded database successfully.")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        seed()