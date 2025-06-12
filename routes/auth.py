# Finalproject/routes/auth.py
from flask import request, jsonify, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db, bcrypt # Adjusted: Imported bcrypt from app.extensions, removed werkzeug.security imports
from app.models import User # This import remains correct

auth_bp = Blueprint("auth_bp", __name__)

# Supporting function to serialize User objects
def serialize_user(user_obj): 
        return {
        'id': user_obj.id,
        'email': user_obj.email,
        'firstName': user_obj.first_name,
        'lastName': user_obj.last_name,
        'role': user_obj.role,
    }
@auth_bp.route('/register', methods=["POST"])
def register():
    data = request.get_json()
    # Check if user already exists
    # If the provided email is missing, data.get('email') would be None, leading to an error
    # The validation for missing email below handles this.
    if data and data.get('email') and User.query.filter_by(email=data["email"]).first(): # check for data and data.get('email') to prevent KeyError if email is missing entirely
        return jsonify({'message':'User with this email already exists'}), 409 
    
    # Store user's input
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    role = data.get('role', 'student') # Default to 'student' if not provided

    # --- Input Validation ---
    missing_fields = []
    if not email:
        missing_fields.append('email')
    if not password:
        missing_fields.append('password')
    if not first_name:
        missing_fields.append('first_name')
    if not last_name:
        missing_fields.append('last_name')

    if missing_fields:
        return jsonify(message=f"Missing required fields: {', '.join(missing_fields)}"), 400
        
    # Email format basic validation (optional but good)
    if not "@" in email or not "." in email:
        return jsonify(message="Invalid email format"), 400
        
    # Validate role (if not already done via decorator/config, ensuring consistency)
    allowed_roles = ['admin', 'instructor', 'student']
    if role not in allowed_roles:
        return jsonify(message=f"Invalid role specified. Allowed roles are: {', '.join(allowed_roles)}"), 400 # Adjusted: Added role validation

    # Hash password using Flask-Bcrypt's generate_password_hash
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8') # Adjusted: Used bcrypt from app.extensions and 'password' variable

    user = User(
        email=email,
        password_hash=hashed_password,
        first_name=first_name,
        last_name=last_name,
        role=role
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'message':'User registered successfully', 'user': serialize_user(user)}), 201

@auth_bp.route('/login', methods=["POST"])
def login():
    data = request.get_json()
    if not data: 
        return jsonify(message="No input data provided or invalid JSON"), 400

    email = data.get('email') 
    password = data.get('password') 

    if not email or not password: # Combined checks for missing email or password
        return jsonify(message="Email and password are required"), 400

    user = User.query.filter_by(email=email).first() 

    if not user or not bcrypt.check_password_hash(user.password_hash, password): # Used bcrypt.check_password_hash and 'password' variable
        return jsonify({'message':'Invalid credentials'}), 401 
    
    login_user(user)



    return jsonify({'message':'Login successful', 'user': serialize_user(user)}) 

@auth_bp.route('/logout', methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({'message':'Logged out successfully'})