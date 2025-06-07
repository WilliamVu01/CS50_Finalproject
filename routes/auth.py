# Finalproject/routes/auth.py
from flask import request, jsonify, Blueprint
from werkzeug.security import generate_password_hash
from app.models import User # This import remains correct
from app.extensions import db # <--- Import db from extensions

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route('/auth/register', methods=["POST"])
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