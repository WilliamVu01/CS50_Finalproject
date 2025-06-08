from flask import Flask, jsonify
from dotenv import load_dotenv
import os

# Import relevant function/routes into Flask app
from .extensions import db, migrate, login_manager
from .models import User
from routes.auth import auth_bp
from routes.admin import admin_bp

def create_app():

    # Load env variables to app
    load_dotenv()


    # initializes Flask app and connect all components inside app/ together
    # loads .env file configurations (from config.py)
    # initializes extensions (SQLAlchemy, Flask-Login, Migrate), and registers routes
    # register blueprints/routes from routes.py

    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register Blueprint for route
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/ping') # This is the line that's causing the error
    def ping():
        return {'message': 'pong'}, 200

    @app.route('/debug/routes')
    def debug_routes():
        output = []
        for rule in app.url_map.iter_rules():
            methods = ','.join(rule.methods - {'HEAD', 'OPTIONS'})
            line = f"Endpoint: {rule.endpoint} | Methods: {methods} | URL: {rule.rule}"
            output.append(line)
        return jsonify(output)

    return app