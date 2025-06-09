from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

from app.extensions import db, bcrypt
from itls.decorators import roles_required
from app.models import TrainingElement

training_elements_bp = Blueprint("training_elements_bp",__name__)
print(f"DEBUG: training_elements_bp is initialized successfully with name: {training_elements_bp}")

# Function for serializing training elements
def serialize_training_elements(training_element):
    return {
        'id': training_element.id,
        'name': training_element.name,
        'description': training_element.description, 
        'duration_minutes': training_element.duration_minutes, 
        'session_type': training_element.session_type, 
        'material_link': training_element.material_link, 
        'created_at': training_element.created_at.isoformat() if training_element.created_at else None, 
        'updated_at': training_element.updated_at.isoformat() if training_element.updated_at else None 
    }


# View training elements for all user
@training_elements_bp.route('/', methods=["GET"])
def get_training_element():
    try:
        training_elements = TrainingElement.query.all()
        if not training_elements:
            return jsonify([serialize_training_elements(element_obj) for element_obj in training_elements]), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error fetching training elements:  {e}")
        return jsonify(message="Internal server error", error=str(e)), 500

# Create new training element for admins/user
    # Requires 'name', 'description', 'duration_minutes', 'session_type'
@training_elements_bp.route('/', methods=["POST"])
@login_required
@roles_required('admin', 'instructor')
def create_training_element():
    try:
        # Initialize data object to obtain user's HTTP request
        data = request.get_json()      
        if not data:
            return jsonify("No input data provided"), 400
        name = data.get('name')
        decription = data.get('decription')
        duration_minutes = data.get('duration_minutes')
        session_type = data.get('session_type')
        material_link = data.get('material_link')
        
        if not name or not decription or duration_minutes is None or not session_type:
            return jsonify("Missing required field: 'name', 'description', 'duration_minutes', 'session_type' "), 400
        if duration_minutes < 0 or isinstance(duration_minutes, int):
            return jsonify("Duration must be positive number"), 400
        new_element = TrainingElement(
            name = name,
            decription = decription,
            duration_minutes = duration_minutes,
            session_type = session_type,
            material_link = material_link
        )
        db.session.add(new_element)
        db.session.commit()
        return jsonify("Training element is created successfully", element=serialize_training_elements(new_element)), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error in creating new training element")
        return jsonify(message="Internal sever error", error=str(e))
    
# Manage training elements for instructors & admins
# Retrieve training element information
@training_elements_bp.route('/<int:element_id>', methods="GET")
@login_required
@roles_required('admin', 'instructor')
def get_training_element_by_id(element_id):
    try:
        training_element = TrainingElement.query.get(element_id)
        if not training_elements:
            return jsonify("Training element not found"), 404
        return jsonify(serialize_training_elements(training_elements)), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error fetching training element infor")
        return jsonify(" Interal sever error"), 500
# Update training elements for Instructor only
@training_elements_bp.route('\<int:element_id>', methods="PUT")
@login_required
@roles_required('instructor')
def update_training_element_by_id(element_id):
    try:
        training_element = TrainingElement.query.get(element_id)
        if not training_element:
            return jsonify("Training element not found"), 404
        data = request.get_json()
        if not data:
            return jsonify("No input data provided"), 400
        if 'name' in data:
            training_element.name = data['name']
        if 'decription' in data:
            training_element.decription = data['decription']
        if 'duration_minutes' in data:
            duration_minutes = data['duration_minutes']
            if duration_minutes < 0 or isinstance(duration_minutes, int):
                return jsonify("Duration must be positive number"), 400
            training_element.duration_minutes = data['duration_minutes']
        if 'session_type' in data:
            training_element.session_type = data['session_type']
        training_element.updated_at = db.func.now()
        db.session.commit()
        return jsonify("Training element is updated successfully", training_element = serialize_training_elements(training_element)), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error fetching training element infor")
        return jsonify(" Interal sever error"), 500
# Delete training elements for Instructor only
@training_elements_bp.route('\<int:element_id>', methods="DELETE")
@login_required
@roles_required('instructor')
def delete_training_element_by_id(element_id):
    try:
        training_element = TrainingElement.query.get(element_id)
        if not training_element:
            return jsonify("Training element not found"), 404
        if current_user.role != 'instructor':
            return jsonify("You are not authorized to delete the training element"), 400
        
        db.session.delete(training_element)
        db.session.commit()
        return jsonify("Training element deleted successfully"), 204 # Server completed successfully but not return any content
    except Exception as e:
        db.session.rollback()
        print(f"Error fetching training element infor")
        return jsonify(" Interal sever error"), 500
