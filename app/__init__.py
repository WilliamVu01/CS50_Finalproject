# Finalproject/app/__init__.py

import os
from flask import Flask, jsonify
from dotenv import load_dotenv # Import load_dotenv
from flask_cors import CORS
from werkzeug.exceptions import BadRequest, Unauthorized, Forbidden, NotFound, InternalServerError

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
      # For Prod: CORS(app, supports_credentials=True, origins=["http://localhost:5173", "http://127.0.0.1:5000"])
    CORS(app, supports_credentials=True) # For dev to resolve issue

    # Configure Flask-Login's user loader


    @login_manager.user_loader
        # user_loader function tells Flask-Login how to reload a user object from a user ID stored in the session.
        # when a user successfully logs in , Flask-Login stores their unique ID in the session cookie.
    def load_user(user_id):
        return User.query.get(user_id) 
        # This function tells Flask-Login how to load a user from the database given their ID.
        # Pass it as a string from session to load_user
    
   # --- Centralized Error Handlers ---
        # These handlers provide consistent JSON responses for various HTTP error codes.
            #  easier for frontend (React) or other API consumer to parse and react to errors predictably.
            # Improved User Experience (Frontend): When frontend receives a consistent JSON error, it can display meaningful messages to the user 
        # Centralized handlers allow you to control exactly what information is returned in error messages:
        #   # preventing sensitive details from leaking, especially in production environment
        # Catch various types of errors: not just from your explicit if conditions, but from underlying Flask operations or other third-party libraries
        # Prevents partial or corrupted data from being saved, maintaining database integrity.
        # Note: Flask-Login's unauthorized_handler will still take precedence for errors
    

    @app.errorhandler(400)
    def bad_request_error(error):
        # Werkzeug's BadRequest exception (often raised by request.json if malformed)
        # can carry a description. Use it if available, otherwise a generic message.
        return jsonify(message=getattr(error, 'description', 'Bad Request: The server cannot process the request due to a client error.')), 400
    # Handle Flask-Login's direct authentication check from app's extension
    @app.errorhandler(401)
    def unauthorized_error(error):
        # Catches 401s not handled by Flask-Login's specific unauthorized_handler
        return jsonify(message=getattr(error, 'description', 'Unauthorized: Authentication required or invalid credentials.')), 401

    @app.errorhandler(403)
    def forbidden_error(error):
        # Catches 403s raised by Flask or explicitly aborted in views/decorators
        return jsonify(message=getattr(error, 'description', 'Forbidden: You do not have permission to access the requested resource.')), 403

    @app.errorhandler(404)
    def not_found_error(error):
        # Catches 404s for non-existent URLs or resources
        return jsonify(message=getattr(error, 'description', 'Not Found: The requested URL or resource was not found on the server.')), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        # Ensures a database rollback on any internal server error that propagates up
        db.session.rollback()
        return jsonify(message="Internal Server Error", error=str(error) if app.debug else "An unexpected error occurred"), 500

    # Configure Flask-Login's unauthorized handler for API requests.
        # Prevent default redirect behavior from Flask-Login
        # API request don't want a direct
        # React app expects a JSON response with an appropriate HTTP status code so it can handle the error programmatically
            # If  API redirects with an HTML response
            # # Frontend JavaScript won't understand it, potentially leading to CORS errors or unexpected behavior.
    @login_manager.unauthorized_handler 
    def unauthorized():
        return jsonify(message="Unauthorized: Login required."), 401


    # Import blueprint
    from routes.auth import auth_bp 
    from routes.admin import admin_bp
    from routes.users import users_bp
    from routes.training_elements import training_elements_bp
    from routes.bookings import bookings_bp

    # Register Blueprints for your API routes with URL prefixes.
    # Using url_prefix is a best practice for organizing API endpoints and preventing conflicts.
    # For example, auth routes will be under /api/auth (e.g., /api/auth/login).
    app.register_blueprint(auth_bp, url_prefix='/api/auth', strict_slashes=False) # ADDED url_prefix
    app.register_blueprint(admin_bp, url_prefix='/api/admin', strict_slashes=False)
    app.register_blueprint(users_bp, url_prefix='/api/users', strict_slashes=False)
    app.register_blueprint(training_elements_bp, url_prefix='/api/training_elements', strict_slashes=False)
    app.register_blueprint(bookings_bp, url_prefix='/api/bookings', strict_slashes=False) 
    
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

    return app
