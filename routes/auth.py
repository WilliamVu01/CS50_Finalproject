# Finalproject/routes/auth.py
from flask import request, jsonify, Blueprint
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User # This import remains correct
from app.extensions import db # <--- Import db from extensions

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route('/register', methods=["POST"])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({'msg':'Email already exist'}), 409

    hashed_password = generate_password_hash(data['password'])

    user = User(
        email=data['email'],
        password_hash=hashed_password,
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        role=data.get('role', 'student')
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'msg':'User register successfully'}), 201

@auth_bp.route('/login', methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'msg':'Invalid incredential'}), 401
    login_user(user)
    return jsonify({'msg':'Login successfully', 'user':user.email})

@auth_bp.route('/logout', methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({'msg':'Logout successfully'})
