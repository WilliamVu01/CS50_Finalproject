from app import db, create_app
from app.models import User, TrainingElement, Booking
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

def seed():
    # Drop and recreate all tables
    db.drop_all()
    db.create_all()

    # Create users
    admin = User(
        email='admin@example.com',
        password_hash=generate_password_hash('admin123'),
        first_name='Admin',
        last_name='William',
        role='admin'
    )

    instructor = User(
        email='instructor@example.com',
        password_hash=generate_password_hash('teachpass'),
        first_name='Jimmy',
        last_name='Le',
        role='instructor'
    )

    student = User(
        email='student@example.com',
        password_hash=generate_password_hash('studentpass'),
        first_name='Brian',
        last_name='Nguyen',
        role='student'
    )

    db.session.add_all([admin, instructor, student])
    db.session.commit()

    # Create training elements
    te1 = TrainingElement(
        name='Mould TPM',
        description='Mould cleaning',
        duration_minutes=60,
        session_type='Classroom',
        material_link='https://example.com/mould-tpm'
    )

    te2 = TrainingElement(
        name='Machine TPM',
        description='Machine cleanning and practice.',
        duration_minutes=45,
        session_type='Practice',
        material_link='https://example.com/machine-tpm'
    )

    db.session.add_all([te1, te2])
    db.session.commit()

    # Create bookings
    now = datetime.utcnow()
    booking1 = Booking(
        training_element_id=te1.id,
        instructor_id=instructor.id,
        student_id=student.id,
        start_time=now + timedelta(days=2),
        end_time=now + timedelta(days=2, minutes=te1.duration_minutes)
    )

    booking2 = Booking(
        training_element_id=te2.id,
        instructor_id=instructor.id,
        student_id=student.id,
        start_time=now + timedelta(days=3),
        end_time=now + timedelta(days=3, minutes=te2.duration_minutes)
    )

    db.session.add_all([booking1, booking2])
    db.session.commit()

    print("✅ Seeded database successfully.")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        seed()
