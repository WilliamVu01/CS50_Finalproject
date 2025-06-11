# Finalproject/app/__init__.py

import os
from flask import Flask, jsonify
from dotenv import load_dotenv # Import load_dotenv
from flask_cors import CORS

# Load environment variables early, before app creation.
# This ensures they are available for configuration.
load_dotenv()
# Import extensions and models
from .extensions import db, migrate, login_manager, bcrypt
from .models import User # User model is imported here to be accessible for user_loader


# The create_app function now accepts a config_object argument.
# This allows you to pass different configuration classes (e.g., DevelopmentConfig, TestingConfig)
# when creating the app instance, making your application more flexible for different environments.
def create_app(config_object='config.DevelopmentConfig'): # ADDED config_object argument
    app = Flask(__name__)
    # Load configurations from the specified config object (e.g., config.DevelopmentConfig from config.py)
    app.config.from_object(config_object) # USING config_object here

    # Initialize extensions with the Flask app instance
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Configure CORS - allows your React frontend to make requests
    # Adjust origins as needed for production (e.g., your frontend domain)
    # The `supports_credentials=True` is important for session cookies with Flask-Login
    CORS(app, supports_credentials=True, origins=["http://localhost:5173", "http://127.0.0.1:5173"])

    # Configure Flask-Login's user loader
    # This function tells Flask-Login how to load a user from the database given their ID.
    # IMPORTANT: User IDs are UUIDs (strings) in your models, so do NOT convert to int.
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id) # REMOVED int() cast

    # Configure Flask-Login's unauthorized handler for API requests.
    # This is crucial for an API-only backend. Instead of redirecting to a login page,
    # it returns a JSON response with a 401 Unauthorized status.
    @login_manager.unauthorized_handler # ADDED unauthorized handler
    def unauthorized():
        return jsonify(message="Unauthorized: Login required."), 401


    # Import extensions and models
    from routes.auth import auth_bp 
    from routes.admin import admin_bp
    from routes.users import users_bp
    from routes.training_elements import training_elements_bp
    from routes.bookings import bookings_bp

    # Register Blueprints for your API routes with URL prefixes.
    # Using url_prefix is a best practice for organizing API endpoints and preventing conflicts.
    # For example, auth routes will be under /api/auth (e.g., /api/auth/login).
    app.register_blueprint(auth_bp, url_prefix='/api/auth') # ADDED url_prefix
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(training_elements_bp, url_prefix='/api/training_elements')
    app.register_blueprint(bookings_bp, url_prefix='/api/bookings') 
    
    # Example: Register other blueprints as they are created
    # from routes.users import users_bp # Example: from routes.users if users.py is in Finalproject/routes
    # app.register_blueprint(users_bp, url_prefix='/api/users')
    # from routes.training_elements import training_elements_bp
    # app.register_blueprint(training_elements_bp, url_prefix='/api/training-elements')
    # from routes.bookings import bookings_bp
    # app.register_blueprint(bookings_bp, url_prefix='/api/bookings')

    # Basic root route for testing server status
    @app.route('/')
    def index():
        return jsonify(message='Welcome to the Training Scheduling API!')

    # User's existing health check route
    @app.route('/ping')
    def ping():
        return {'message': 'pong'}, 200

    # User's existing route to debug all registered routes
    @app.route('/debug/routes')
    def debug_routes():
        output = []
        for rule in app.url_map.iter_rules():
            # Exclude OPTIONS and HEAD methods for cleaner output
            methods = ','.join(rule.methods - {'HEAD', 'OPTIONS'})
            line = f"Endpoint: {rule.endpoint} | Methods: {methods} | URL: {rule.rule}"
            output.append(line)
        return jsonify(output)

    # Register a generic error handler for 500 (Internal Server Error).
    # This provides a consistent JSON response for unhandled exceptions,
    # and avoids leaking sensitive stack traces in production.
    @app.errorhandler(500) # ADDED 500 error handler
    def internal_server_error(e):
        # In production, avoid sending full error details; just a generic message
        return jsonify(message="Internal Server Error", error=str(e) if app.debug else "An unexpected error occurred"), 500

    return app
