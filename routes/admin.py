from flask import request, Blueprint, jsonify
from itls.decorators import role_required


admin_bp = Blueprint("admin_bp", __name__)
print(f"DEBUG: admin_bp initialized with name: {admin_bp.name}") 

@admin_bp.route('/auth/admin-only', methods=["GET"])
@role_required('admin')
def admin():

    return jsonify({'msg':'Welcome ADMIN'})

