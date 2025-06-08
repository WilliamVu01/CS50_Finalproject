from flask import request, Blueprint, jsonify
from itls.decorators import roles_required


admin_bp = Blueprint("admin_bp", __name__)
# exclusively for administrators and often involve higher-level system management or specific admin dashboards.
# typically for admin-specific views or actions related to users, not the generic CRUD.
print(f"DEBUG: admin_bp initialized with name: {admin_bp.name}") 

@admin_bp.route('/admin-only', methods=["GET"])
@roles_required('admin')
def admin():

    return jsonify({'msg':'Welcome ADMIN'})

