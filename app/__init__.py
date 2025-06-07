# Finalproject/app/__init__.py
from flask import Flask, jsonify
from dotenv import load_dotenv
import os

from .extensions import db, migrate, login_manager
from .models import User
from routes.auth import auth_bp

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    app.register_blueprint(auth_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # ADD THIS LINE FOR DEBUGGING
    print(f"DEBUG: Type of 'app' before routes: {type(app)}")

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