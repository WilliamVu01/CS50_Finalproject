from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.extensions import db, bcrypt
from itls.decorators import roles_required
from app.models import User

users_bp = Blueprint("users_bp", __name__)
print(f"DEBUG: users_bp is initialized with name: {users_bp.name}")

# SQLAlchemy objects are not directly JSON serializable.
# Need to convert each User object into a dictionary (or a similar serializable format) first
# User (id, email, password_hash, first_name, last_name, role: admin/instructor/student, created_at, updated_at)
def serialize_user(user):
    """
    Serializes a User SQLAlchemy object into a dictionary for JSON response.
    """
    return {
        'id': user.id,
        'email': user.email,
        'firstName': user.first_name,
        'lastName': user.last_name,
        'role': user.role,
        'createdAt': user.created_at.isoformat() if user.created_at else None,
        'updatedAt': user.updated_at.isoformat() if user.updated_at else None
    }
# List all of user's detail (GET)
@users_bp.route('/')
@login_required # Requires user to login
@roles_required('admin') # Requires 'admin' role to access this route
def get_all_users():
    """
    GET /api/users
    Retrive all users.  Granted to Admin role only
    """
    try:
        users = User.query.all()
        return jsonify([serialize_user(user_obj) for user_obj in users]), 200
    except Exception as e:
        # discards all the staged changes and reverts the database to the state it was in before the transaction began.
        db.session.rollback()  # Ensure rollback on error
        print(f"Error fetching all users: {e}")
        return jsonify(message="Internal server error", error=str(e)), 500

# Modify user's information like role/email (PUT)

    # Flask's routing mechanism (provided by Werkzeug) examines the incoming URL path 
    # and tries to match it against its registered patterns in '__init__.py'
    # Flask's router sees the pattern: /api/users/<int:user_id> it matches the literal parts /api/users/.

# Get user information 
@users_bp.route('/<int:user_id>', methods=["GET"]) # int is URL converter whom conver user_id to integer then pass function
@login_required
def get_user_by_id(user_id): # get_userinfo_by_id function receive 'user_id' as a argument 

    try:
        # retrieve a user record directly from user_id, if not return None
        # user is an object as an instance of User model for specific 'user_id'
        # E.g: user.emal; user.first_name
        # 'user' object is attached to 'db.session'
        user = User.query.get(user_id)
        if not user:
            return jsonify(message="User not found"), 404
        # current_user proxy available after login_required passed
        # current_user object represents the actual User model instance of the person who logged in
        if current_user.role != 'admin' and current_user.id != user_id:
            return jsonify(message="You can only view your own profile unless you are a admin"), 403
        
        return jsonify(serialize_user(user)), 200
    except Exception as e:
        # discards all the staged changes and reverts the database to the state it was in before the transaction began.
        db.session.rollback()
        print(f"Error fetching user's information: {e}")
        return jsonify(message="Internal sever error", error=str(e)), 500
# Update user information using PUT (not using PATCH sinc PUT coudl cover all scope)
@users_bp.route('/<int:user_id>', methods=["PUT"])    
def update_user_by_id(user_id):
    
    try:
        #'user' is a Python object in memory. It is attached to 'db.session'
        user = User.query.get(user_id)
        if not user:
            return jsonify("User not found"), 404
        # Initialize data object to obtain user's HTTP request
        data = request.get_json()
        if not data:
            return jsonify("Data is not provided"), 400
        # Verify the authentification as a admin for this route
        if current_user.role != 'admin' and current_user.id != user_id:
            return jsonify(message="Access denied: You only view your own profile unless you are a admin"), 403
        
        # Update user's info for normal user such email/first_name/last_name
        # using [key in dictionary] method to update user's info at each User model field when it exists
        if 'email' in data:
            user.email = data['email']
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'password' in data and data['password']:
            user.password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        # Update user's info with 'admin' access
        if 'role' in data:
            if current_user.role != 'admin':
                return jsonify(message="Only a admin can change user role"), 403
            allowed_roles = ['admin','instructor','student']
            if data['role'] not in allowed_roles:
                return jsonify(message="Invalid role change, Allowed roles are admin, instructor and student"), 400
            user.role = data['role']
        # Reflect lasted updated_time 
        user.updated_at = db.func.now()
        # Commit change request into database since 'user' object is attached to 'db.session'
            # db.session is an isolated session within this specific HTTP request in this app
            # any change in 'user' object being reflected in 'db.session'
            # 'db.session' being commited meaning that the changes move from memory to database
            # this is the point where SQLAlchemy generates the necessary SQL statements (INSERTs, UPDATEs, DELETEs)
            # and sends them to database (schedulingapp.db)
        db.session.commit()
        # Inform change status and visualize the latest info
        return jsonify(message="Updated successfully", user=serialize_user(user)), 200
    except Exception as e:
        # discards all the staged changes and reverts the database to the state it was in before the transaction began.
        db.session.rollback()
        print(f"Error in updating user's information: {e}")
        return jsonify(message="Internal server error", error=str(e)), 500
# Enable the capability for a 'admin' only to delete user if no longer need (DELETE)
@users_bp.route('/<int:user_id>', methods=["DELETE"])
@login_required
@roles_required('admin')
def delete_user_by_id(user_id):
    try:
        user = User.query.get(user_id)

        if not user:
            return jsonify(message="User not found"), 404
        # Prevent a admin delete itself
        if current_user.id == user_id:
            return jsonify("You cannot delete yourself as a admin"), 400

        db.session.delete(user)
        db.session.commit()
        return jsonify("User deleted successfully"), 204 # Server completed successfully but not return any content

    except Exception as e:
        # discards all the staged changes and reverts the database to the state it was in before the transaction began.
        db.session.rollback()
        print(f"Error deleting user: {e}")
        return jsonify(message="Internal server error", error=str(e)), 500