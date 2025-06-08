from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.extensions import db
from itls.decorators import roles_required
from app.models import User

users_bp = Blueprint("users_bp", __name__)
print(f"DEBUG: users_bp is initialized with name: {users_bp.name}")
# SQLAlchemy objects are not directly JSON serializable.
# need to convert each User object into a dictionary (or a similar serializable format) first
def serialize_user(user):
    """
    Serializes a User SQLAlchemy object into a dictionary for JSON response.
    """
    return {
        'id': str(user.id), # Ensure UUID is stringified
        'email': user.email,
        'firstName': user.first_name,
        'lastName': user.last_name,
        'role': user.role,
        'createdAt': user.created_at.isoformat() if user.created_at else None,
        'updatedAt': user.updated_at.isoformat() if user.updated_at else None
    }



# List all of user's detail (GET)
@users_bp.route('/')
@login_required
@roles_required('admin')
def get_all_user():
    try:
        users = User.query.all()
        return jsonify([serialize_user(user_obj) for user_obj in users]), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error fetching all users: {e}")
        return jsonify(message="Internal server error", error=str(e)), 500



# modify user's information like role/email (PUT)

# enable the capability for user to delete user if no longer need (DELETE)
