# --- Start of Flask Shell Script ---

from app import create_app, db
from app.models import TrainingElement, User
from dotenv import load_dotenv
import os

# Ensure environment variables are loaded
load_dotenv()

# Create and push app context to allow database operations
app = create_app()
app.app_context().push()

print("--- Initializing Database Data ---")

# --- Add Test Users (Instructor and Student) ---
# Passwords are 'password' for both
# Checks if users already exist to prevent duplicates

# Instructor: Jimmy Nguyen
instructor_email = 'testinstructor@example.com' # Reverted to your original specified instructor email
user_instructor = User.query.filter_by(email=instructor_email).first()
if not user_instructor:
    user_instructor = User(email=instructor_email, first_name='Jimmy', last_name='Nguyen', role='instructor')
    user_instructor.set_password('password')
    db.session.add(user_instructor)
    db.session.commit() # Commit immediately to get an ID for relationships if needed later
    print(f"Created instructor: {user_instructor.email}")
else:
    print(f"Instructor '{instructor_email}' already exists.")

# Student: Brian Le
student_email = 'teststudent@example.com' # Reverted to your original specified student email
user_student = User.query.filter_by(email=student_email).first()
if not user_student:
    user_student = User(email=student_email, first_name='Brian', last_name='Le', role='student')
    user_student.set_password('password')
    db.session.add(user_student)
    db.session.commit() # Commit immediately
    print(f"Created student: {user_student.email}")
else:
    print(f"Student '{student_email}' already exists.")

# --- Add Training Elements ---
# Checks if elements already exist to prevent duplicates

elements_to_add = [
    {'name': 'Basic Python', 'description': 'Introduction to Python programming.', 'duration_minutes': 90, 'session_type': 'classroom', 'material_link': 'http://example.com/python-materials'},
    {'name': 'Advanced SQL', 'description': 'Deep dive into SQL queries and optimization.', 'duration_minutes': 120, 'session_type': 'hands_on', 'material_link': 'http://example.com/sql-materials'},
    {'name': 'React Fundamentals', 'description': 'Building blocks of React applications.', 'duration_minutes': 180, 'session_type': 'e_learning', 'material_link': 'http://example.com/react-course'},
    {'name': 'Cloud Computing Basics', 'description': 'Introduction to cloud platforms and services.', 'duration_minutes': 60, 'session_type': 'classroom', 'material_link': 'http://example.com/cloud-intro'}
]

for elem_data in elements_to_add:
    if not TrainingElement.query.filter_by(name=elem_data['name']).first():
        element = TrainingElement(**elem_data)
        db.session.add(element)
        print(f"Added training element: {elem_data['name']}")
    else:
        print(f"Training element '{elem_data['name']}' already exists.")

db.session.commit()
print("Training elements and sample users added/ensured.")

# --- Verification ---
print("\n--- Verification ---")

print("\nAll Training Elements:")
for te in TrainingElement.query.all():
    print(f"  - {te.name} ({te.duration_minutes} min)")

print("\nAll Users:")
for u in User.query.all():
    print(f"  - {u.first_name} {u.last_name} ({u.email}) - {u.role}")

print("\n--- Database setup complete ---")

# --- End of Flask Shell Script ---
# --- Start of Flask Shell Script ---

from app import create_app, db
from app.models import TrainingElement, User
from dotenv import load_dotenv
import os

# Ensure environment variables are loaded
load_dotenv()

# Create and push app context to allow database operations
app = create_app()
app.app_context().push()

print("--- Initializing Database Data ---")

# --- Add Test Users (Instructor and Student) ---
# Passwords are 'password' for both
# Checks if users already exist to prevent duplicates

# Instructor: Jimmy Nguyen
instructor_email = 'instructortest@example.com' # Reverted to your original specified instructor email
user_instructor = User.query.filter_by(email=instructor_email).first()
if not user_instructor:
    user_instructor = User(email=instructor_email, first_name='Jimmy', last_name='Nguyen', role='instructor')
    user_instructor.set_password('password')
    db.session.add(user_instructor)
    db.session.commit() # Commit immediately to get an ID for relationships if needed later
    print(f"Created instructor: {user_instructor.email}")
else:
    print(f"Instructor '{instructor_email}' already exists.")

# Student: Brian Le
student_email = 'teststudent@example.com' # Reverted to your original specified student email
user_student = User.query.filter_by(email=student_email).first()
if not user_student:
    user_student = User(email=student_email, first_name='Brian', last_name='Le', role='student')
    user_student.set_password('password')
    db.session.add(user_student)
    db.session.commit() # Commit immediately
    print(f"Created student: {user_student.email}")
else:
    print(f"Student '{student_email}' already exists.")

# --- Add Training Elements ---
# Checks if elements already exist to prevent duplicates

elements_to_add = [
    {'name': 'Basic Python', 'description': 'Introduction to Python programming.', 'duration_minutes': 90, 'session_type': 'classroom', 'material_link': 'http://example.com/python-materials'},
    {'name': 'Advanced SQL', 'description': 'Deep dive into SQL queries and optimization.', 'duration_minutes': 120, 'session_type': 'hands_on', 'material_link': 'http://example.com/sql-materials'},
    {'name': 'React Fundamentals', 'description': 'Building blocks of React applications.', 'duration_minutes': 180, 'session_type': 'e_learning', 'material_link': 'http://example.com/react-course'},
    {'name': 'Cloud Computing Basics', 'description': 'Introduction to cloud platforms and services.', 'duration_minutes': 60, 'session_type': 'classroom', 'material_link': 'http://example.com/cloud-intro'}
]

for elem_data in elements_to_add:
    if not TrainingElement.query.filter_by(name=elem_data['name']).first():
        element = TrainingElement(**elem_data)
        db.session.add(element)
        print(f"Added training element: {elem_data['name']}")
    else:
        print(f"Training element '{elem_data['name']}' already exists.")

db.session.commit()
print("Training elements and sample users added/ensured.")

# --- Verification ---
print("\n--- Verification ---")

print("\nAll Training Elements:")
for te in TrainingElement.query.all():
    print(f"  - {te.name} ({te.duration_minutes} min)")

print("\nAll Users:")
for u in User.query.all():
    print(f"  - {u.first_name} {u.last_name} ({u.email}) - {u.role}")

print("\n--- Database setup complete ---")

# --- End of Flask Shell Script ---
