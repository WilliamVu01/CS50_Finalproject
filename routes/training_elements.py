from flask import Blueprint, request, jsonify
from flask_login import login_required
from flask_cors import cross_origin

from app.extensions import db
from itls.decorators import roles_required
from app.models import TrainingElement

training_elements_bp = Blueprint("training_elements_bp",__name__)

print(f"DEBUG: training_elements_bp is initialized with name: {training_elements_bp.name}")

# ----Overall----
# Any loggined user can retrieve training elements
# Only 'instructor' can perform "create" , "update"  & "delete" training elements


# Function for serializing training elements
# TrainingElement (id, name, description, duration_minutes, session_type, material_link, created_at, updated_at)
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
@training_elements_bp.route('/', methods=["GET"], strict_slashes=False)
def get_training_element():
    try:
        training_elements = TrainingElement.query.all()
        if not training_elements:
            return jsonify(message="Training element not found"), 404
        return jsonify([serialize_training_elements(element_obj) for element_obj in training_elements]), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error fetching training elements:  {e}")
        return jsonify(message="Internal server error", error=str(e)), 500


# Create new training element for admins/user
    # Requires 'name', 'description', 'duration_minutes', 'session_type'
@training_elements_bp.route('/', methods=["POST"], strict_slashes=False)
@cross_origin(supports_credentials=True, origins=["http://127.0.0.1:5173", "http://localhost:5173"]) # Create by AI: Add cross_origin decorator to handle preflight
@login_required
@roles_required('admin', 'instructor')
def create_training_element():
    try:
        # Initialize data object to obtain user's HTTP request
        data = request.get_json()      
        if not data:
            return jsonify(message="No input data provided"), 400
        
        name = data.get('name')
        description = data.get('description')
        duration_minutes = data.get('duration_minutes')
        session_type = data.get('session_type')
        material_link = data.get('material_link')
        
        # Input Validation
        missing_fields = []
        if not name:
            missing_fields.append('name')
        if not description:
            missing_fields.append('description')
        if duration_minutes is None: # Check for None, as 0 might be a valid duration in other contexts
            missing_fields.append('duration_minutes')
        if not session_type: # session_type is now explicitly a required field
            missing_fields.append('session_type')

        if missing_fields:
            return jsonify(message=f"Missing required fields: {', '.join(missing_fields)}"), 400
        
        allowed_session_types = ['classroom', 'hands_on', 'e_learning', 'assessment']
        if session_type not in allowed_session_types:
            return jsonify("session type is invalid, input allowed types: classroom, hands_on, e_learning, assessment"), 400
        if duration_minutes <= 0 or not isinstance(duration_minutes, int):
            return jsonify(message="Duration must be positive number"), 400
        
        new_element = TrainingElement(
            name = name,
            description = description,
            duration_minutes = duration_minutes,
            session_type = session_type,
            material_link = material_link
        )
        db.session.add(new_element)
        db.session.commit()
        return jsonify(message="Training element is created successfully", element=serialize_training_elements(new_element)), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error in creating new training element")
        return jsonify(message="Internal sever error", error=str(e))
# Endpoint to get allowed session types, it will allow fontend to show in the dropdown
@training_elements_bp.route('/session_types', methods=["GET"], strict_slashes=False)
def get_session_types():
    try:
        # Dynamically get enum values from the TrainingElement model
        session_types_enum = TrainingElement.session_type.type.enums
        return jsonify(session_types_enum), 200
    except Exception as e:
        print(f"Error fetching session types: {e}")
        return jsonify(message="Internal server error", error=str(e)), 500
        
# Manage training elements for instructors & admins
# Retrieve training element information
@training_elements_bp.route('/<int:element_id>', methods=["GET"], strict_slashes=False)
@login_required
@roles_required('admin', 'instructor')
def get_training_element_by_id(element_id):
    try:
        training_element = TrainingElement.query.get(element_id)
        if not training_element:
            return jsonify(message="Training element not found"), 404
        return jsonify(serialize_training_elements(training_element)), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error fetching training element infor")
        return jsonify(message="Interal server error"), 500
    
# Update training elements for Instructor only
@training_elements_bp.route('/<int:element_id>', methods=["PUT"], strict_slashes=False)
@login_required
@roles_required('instructor')
def update_training_element_by_id(element_id):
    try:
        training_element = TrainingElement.query.get(element_id)

        if not training_element:
            return jsonify(message="Training element not found"), 404
        data = request.get_json()
        if not data:
            return jsonify(message="No input data provided"), 400
        if 'name' in data:
            training_element.name = data['name']
        if 'decription' in data:
            training_element.description = data['decription']
        if 'duration_minutes' in data:
            duration_minutes = data['duration_minutes']
            if duration_minutes <= 0 or not isinstance(duration_minutes, int):
                return jsonify(message="Duration must be positive number"), 400
            training_element.duration_minutes = data['duration_minutes']
        if 'session_type' in data:
            training_element.session_type = data['session_type']
        if 'material_link' in data:
            training_element.material_link = data['material_link']    
        training_element.updated_at = db.func.now()
        db.session.commit()
        return jsonify(message="Training element is updated successfully", training_element = serialize_training_elements(training_element)), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error fetching training element infor")
        return jsonify(message="Interal server error"), 500
    
# Delete training elements for Instructor only
@training_elements_bp.route('/<int:element_id>', methods=["DELETE"], strict_slashes=False)
@login_required
@roles_required('instructor')
def delete_training_element_by_id(element_id):
    try:
        training_element = TrainingElement.query.get(element_id)
        if not training_element:
            return jsonify(message="Training element not found"), 404
        db.session.delete(training_element)
        db.session.commit()
        return jsonify(message=f"Training element with id {element_id} deleted successfully"), 204 # Server completed successfully but not return any content
    except Exception as e:
        db.session.rollback()
        print(f"Error fetching training element infor")
        return jsonify(message="Interal server error"), 500
