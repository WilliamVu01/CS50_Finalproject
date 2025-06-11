from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime, timedelta


from app.extensions import db, login_manager
from app.models import Booking, TrainingElement, User
from itls.decorators import roles_required


bookings_bp = Blueprint("booking_bp", __name__)
print(f"DEBUG: bookings_bp is initialized with name: {bookings_bp.name}") # Corrected: use .name for blueprint
# ----Overall----
# Any loggined user can retrieve bookings
# Only 'instructor' can perform "create" , "update"  booking
# Deletion:
    #   Admin can delete booking without needs of being booking creator
    #   Instructor can delete the booking if he/she is the booking creator


# Supporting function for serializing booking
    # Booking (id, training_element_id, start_time, end_time, instructor_id, student_id, created_by_user_id, created_at, updated_at)

def serialize_booking(booking):
    return {
        'id': booking.id,
        'trainingElementId': booking.training_element_id,
        'trainingElementName': booking.training_element.name if booking.training_element else None,
        'startTime': booking.start_time.isoformat() if booking.start_time else None, # Ensure .isoformat()
        'endTime': booking.end_time.isoformat() if booking.end_time else None,     # Ensure .isoformat()
        'instructorId': booking.instructor_id,
        'instructorName': f"{booking.instructor.first_name} {booking.instructor.last_name}" if booking.instructor else None,
        'studentId': booking.student_id, 
        'studentName': f"{booking.student.first_name} {booking.student.last_name}" if booking.student else None,
        'status': booking.status,
        'createdById': booking.created_by_user_id,
        'createdByEmail': booking.created_by.email if booking.created_by else None,
        'notes': booking.notes,
        'createdAt':booking.created_at.isoformat() if booking.created_at else None,
        'updatedAt': booking.updated_at.isoformat() if booking.updated_at else None
    }

# Querying exist bookings
@bookings_bp.route('/', methods=["GET"])
@login_required
def get_all_bookings():
    # Query existing booking
    try:
        # create 'query' as a object for dynamic query operation later
        # it acts a query "constructor/builder"
        query = Booking.query
        # use "args" attribute in "request" for geting use's query in the URL
        training_element_name = request.args.get('training_element_name')
        start_time_str = request.args.get('start_time')
        end_time_str = request.args.get('end_time')
        instructor_id = request.args.get('instructor_id', type=int) # Ensure type conversion
        instructor_name = request.args.get('instructor_name')
        student_id = request.args.get('student_id', type=int) # Ensure type conversion
        student_name = request.args.get('student_name')
        status = request.args.get('status')
        created_by_user_id = request.args.get('created_by_user_id', type=int)
        created_by_user_name = request.args.get('created_by_user_name') 


        if training_element_name:
            query = query.join(TrainingElement).filter(TrainingElement.name.ilike(f'%{training_element_name}%')) # ilike for case-insensitive search
        if start_time_str:
            try:
                start_time = datetime.fromisoformat(start_time_str.replace('Z','+00:00'))
                query = query.filter(Booking.start_time >= start_time)
            except ValueError:
                return jsonify(message="Invalid datetime format. Use ISO 8601 (e.g., 'YYYY-MM-DDTHH:MM:SSZ')"), 400
        if end_time_str:
            try:
                end_time = datetime.fromisoformat(end_time_str.replace('Z','+00:00'))
                query = query.filter(Booking.end_time <= end_time)
            except ValueError:
                 return jsonify(message="Invalid datetime format. Use ISO 8601 (e.g., 'YYYY-MM-DDTHH:MM:SSZ')"), 400
        if instructor_id is not None: # Able to handle when key is 0
            query = query.filter(Booking.instructor_id == instructor_id)
        if instructor_name:
            # Join with the User table via the 'instructor' relationship and filter by first_name OR last_name
            # This handles searching for a name that might be in either field
            query = query.join(Booking.instructor).filter(
                db.or_(
                    User.first_name.ilike(f'%{instructor_name}%'),
                    User.last_name.ilike(f'%{instructor_name}%')
                )
            )

        if student_id is not None:
            query = query.filter(Booking.student_id == student_id)
        if student_name:
            # Join with the User table via the 'student' relationship and filter by first_name OR last_name
            query = query.join(Booking.student).filter(
                db.or_(
                    User.first_name.ilike(f'%{student_name}%'),
                    User.last_name.ilike(f'%{student_name}%')
                )
            )

        if status:
            allowed_statuses = ['pending', 'confirmed', 'completed', 'cancelled']
            if status not in allowed_statuses:
                 return jsonify(message=f"Invalid status filter: '{status}'. Allowed statuses are: {', '.join(allowed_statuses)}"), 400
            query = query.filter(Booking.status == status)

        if created_by_user_id is not None:
            query = query.filter(Booking.created_by_user_id == created_by_user_id)
        if created_by_user_name:
            # Join with the User table via the 'created_by' relationship
            query = query.join(Booking.created_by).filter(
                db.or_(
                    User.first_name.ilike(f'%{created_by_user_name}%'),
                    User.last_name.ilike(f'%{created_by_user_name}%')
                )
            )

        # Construct a query for executing
        bookings = query.all()
        return jsonify([serialize_booking(booking) for booking in bookings]), 200

    except Exception as e:
        print(f"Error fetching bookings: {e}")
        db.session.rollback()
        return jsonify(message="Internal server error", error=str(e)), 500
    
# Create new bookings
@bookings_bp.route('/', methods=["POST"])
@login_required
@roles_required('instructor')
def create_bookings():
    try:
        data = request.get_json()
        if not data:
            return jsonify(message="No input data provided"), 400
        # Required fields
        raw_training_element_id = data.get('training_element_id')
        start_time_str = data.get('start_time') # data via an API: dates and times are typically transmitted as strings (e.g., "2025-06-15T10:00:00Z").
        end_time_str = data.get('end_time') # data.get(): Return 'None' if data is not presented
        
        
        # Optional fields
        raw_instructor_id = data.get('instructor_id')
        raw_student_id = data.get('student_id')
        notes = data.get('notes')
        # Asign a default value for status
        status = data.get('status', 'pending')

        # ---Validate user's input---
        # Check for missing
        missing_fields = []
        if raw_training_element_id is None:
            missing_fields.append('training_element_id')
        if not start_time_str:
            missing_fields.append('start_time')
        if not end_time_str:
            missing_fields.append('end_time')
        if missing_fields:
            return jsonify(message=f"Missing required fields: {',' .join(missing_fields)}"), 400
        
        # Check for valid input value
        # Validate training_element_id exists and is correct type
        training_element_id = None
        if raw_training_element_id is not None:
            try:
                training_element_id = int(raw_training_element_id)
            except (ValueError, TypeError):
                return jsonify(message="training_element_id must be a valid integer"), 400
            
        # Check for valid start_time & end_time
        try:
                # convert start_time_str to object for checking with  database format
            start_time = datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
            end_time = datetime.fromisoformat(end_time_str.replace('Z', '+00:00'))
        except ValueError:
            return jsonify(message="Invalid datetime format. Use ISO 8601 (e.g., 'YYYY-MM-DDTHH:MM:SSZ')"), 400
        if end_time <= start_time:
            return jsonify(message="booking end_time must be after start_time"), 400
        
        instructor_id = None
        if raw_instructor_id is not None:
            try:
                instructor_id = int(raw_instructor_id)
                instructor = User.query.get(instructor_id)
                if not instructor:
                    return jsonify(message=f"Instructor with ID: {instructor_id} not found"), 400
            except (ValueError, TypeError):
                return jsonify(message="instructor_id must be a valid integer or null"), 400
            
        student_id = None
        if raw_student_id is not None:
            try:
                student_id = int(raw_student_id)
                student = User.query.get(student_id)
                if not student:
                    return jsonify(message=f"Student with ID: {student_id} not found"), 400
            except (ValueError, TypeError):
                return jsonify(message="student_id must be a valid integer or null"), 400    
        
        allowed_status = ['pending', 'confirmed', 'completed', 'cancelled']
        if status not in allowed_status:
            return jsonify(message=f"invalid status, allowed status: {allowed_status}"), 400
        
    # ----This logic need to RE-ASSESS FOR IMPROVED VERSION since  it look at time dimension only----
    # ------ Further improve if need to look at differeent dimentions such as specific scope(instructor/resource,..)------
        # Retrieve all exist bookings that having
            #  1) start_time of new booking is happen before exist booking in database AND
            #  2) end_time of new booking is happen after exist booking (by design =]] ) AND
            #  3) retrieve all booking for provided 'instructor_id' OR all booking for provided 'student_id'
    
        conflict_bookings = Booking.query.filter(
            start_time < Booking.end_time, #  new booking starts before existing booking ended
            end_time > Booking.start_time,
            db.or_(
                (Booking.instructor_id==instructor_id) if  instructor_id else False, # check existing booking associated with provided 'instructor_id'else no check
                (Booking.student_id==student_id) if student_id else False # check existing booking associated with provided 'student_id'else no check
            )
        ).all()
        # Check conflict booking
        if conflict_bookings:
            return jsonify(message="the booking is conflicted, instructor or student is already booked during this time.",
                           conflict=[serialize_booking(item) for item in conflict_bookings]), 409 
        
        new_booking= Booking(
            training_element_id = training_element_id,
            instructor_id = instructor_id,
            student_id = student_id,
            start_time = start_time,
            end_time = end_time,
            status = status,
            created_by_user_id = current_user.id,
            notes = notes
        )
        db.session.add(new_booking)
        db.session.commit()
        # Ensure 100% new_booking is refreshed from database
        db.session.refresh(new_booking)
        return jsonify(message="Your session is successfully booked", booking=serialize_booking(new_booking)), 201
    except Exception as e:
        print(f"Error creating booking : {e}")
        db.session.rollback()
        return jsonify(message="Internal server error", error=str(e)), 500

# Update existing booking for instructor only, admin is allowed for deleting
@bookings_bp.route('/<int:booking_id>', methods=["PUT"])
@login_required
@roles_required('instructor')
def update_booking_by_id(booking_id):
    try:
        # Retrieve record of booking via 'booking_id'
        booking = Booking.query.get(booking_id)
        if not booking:
            return jsonify(message="No booking data found"), 404
        # Assign original values for conflict detection comparison
        original_start_time = booking.start_time
        original_end_time = booking.end_time
        original_instructor_id = booking.instructor_id
        original_student_id = booking.student_id
        # Get request from user
        data = request.get_json()
        # Validate user's request
        if not data:
            return jsonify(message="No input data found"), 400
        
        if 'training_element_id' in data:
            # Validate valid input data
            
            if 'training_element_id' in data:
                input_training_element_id = data.get('training_element_id')
                if input_training_element_id is not None:
                    try:
                        training_element_id_int = int(input_training_element_id)
                        valid_training_element_id = TrainingElement.query.get(training_element_id_int)
                        if not valid_training_element_id:
                            return jsonify(message=f"Training element with ID: {training_element_id_int} not found"), 400
                        booking.training_element_id = training_element_id_int
                    except (ValueError, TypeError):
                        return jsonify(message="training_element_id must be a valid integer"), 400

        
        if 'instructor_id' in data:
            instructor_id = User.query.get(int(data.get('instructor_id')))
            if not instructor_id:
                return jsonify(message= f"instructor with id: {instructor_id} not found"), 400
            booking.instructor_id = data.get('instructor_id')

        if 'student_id' in data:
            student_id = User.query.get(int(data.get('student_id')))
            if not student_id:
                return jsonify(message=f"student with id: {student_id} not found"), 400
            booking.student_id = data.get('student_id')

        if 'start_time' in data:
            try:
                start_time_str = data.get('start_time')
                booking.start_time = datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
            except ValueError:
                return jsonify(message="Invalid start_time format. Use ISO 8601."), 400
            
        if 'end_time' in data:
            try:
                end_time_str = data.get('end_time')
                booking.end_time = datetime.fromisoformat(end_time_str.replace('Z','+00:00'))
            except ValueError:
                return jsonify(message="Invalid end_time format. Use ISO 8601."), 400
        if booking.start_time >= booking.end_time:
            return jsonify(message="start_time must be before end_time"), 400
        
        if 'status' in data:
            status = data.get('status')
            allowed_status = ['pending', 'confirmed', 'completed', 'cancelled']
            if status not in allowed_status:
                return jsonify(message=f"invalid status, allowed status: {allowed_status}"), 400
            booking.status = status

        if 'notes' in data:
            booking.notes = data.get('notes')
      
        # Re-check Conflict Detection if relevant fields changed
            # Only re-check for conflict if there is change in any of start_time, end_time, instructor_id, or student_id
        if (booking.start_time != original_start_time or
           booking.end_time != original_end_time or
           booking.instructor_id != original_instructor_id or
           booking.student_id != original_student_id):

            conflicting_bookings = Booking.query.filter(
               Booking.id != booking_id,# Exclude the current booking from its own conflict check  & only check with other booking
               Booking.end_time > booking.start_time,
               Booking.start_time < booking.end_time,
               db.or_(
                   Booking.instructor_id == booking.instructor_id if booking.instructor_id else False,
                   Booking.student_id == booking.student_id if booking.student_id else False
               )
           ).all()

            if conflicting_bookings:
                return jsonify(message="Conflict detected: Instructor or student is already booked during this time.",
                            conflicts=[serialize_booking(b) for b in conflicting_bookings]), 409 # 409 Conflict

        booking.updated_at = db.func.now()
        # Commit change to database
        db.session.commit()
        return jsonify(message="Booking updated successfully", booking=serialize_booking(booking)), 200
    except Exception as e:
        print(f"Error fetching bookings")
        db.session.rollback()
        return jsonify(message="Internal server error", error=str(e)), 500

# Delete existing booking
@bookings_bp.route('/<int:booking_id>', methods=["DELETE"])
@login_required
@roles_required('instructor', 'admin')
def delete_booking_by_id(booking_id):
    try:
        booking = Booking.query.get(booking_id)
        if not booking:
            return jsonify(message=f"Booking with id {booking_id} not found"), 404
        # Only allow

        # Authorization logic:
            # Admin can delete any booking.
            # Instructor can delete only bookings they created.
        if current_user.role == 'admin':
            pass # Admin is allowed to delete
        elif current_user.role == 'instructor' and booking.created_by_user_id == current_user.id:
            pass # Instructor can delete if they created it
        else:
            return jsonify(message="Access denied: You must be an admin or the creator of this booking to delete it."), 403 # Changed to 403 Forbidden
        
        db.session.delete(booking)
        db.session.commit()
        return '', 204
    except Exception as e:
        print(f"Error deleting booking {booking_id}: {e}")
        db.session.rollback()
        return jsonify(message="Internal Server Error", error=str(e)), 500