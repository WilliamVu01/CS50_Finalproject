from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

import os

# define models outside of the main app code as a tool to talk to the DB, but connect it to the Flask app later
# utility methods to manage and interact with the database.
db = SQLAlchemy()
# a database migration tool with Flask and SQLAlchemy 
# track changes to database schema and help to apply those changes safely over time, without manually rewriting SQL scripts or losing data
# track database schema changes over time without connect it tightly to the app during initial import
# waits for your app and db to be linked.
migrate = Migrate()
# the tool for handling authentication and authorization in specific route which need to be protected
# Protect routes that require authentication
# Access user identity from the token
# Add custom functionalitty (e.g. roles).
jwt = JWTManager()

# initializes Flask app and connect all components inside app/ together
# loads .env file configurations (from config.py)
# initializes extensions (SQLAlchemy, JWT, Migrate), and registers routes
# register blueprints/routes from routes.py

def create_app():
    load_dotenv()  # load .env file

    app = Flask(__name__)
    app.config.from_object('config.Config')  # load 'Config' class from config.py

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Import and register blueprints here (later)
    from .models import User, TrainingElement, Booking
    @app.route('/ping')
    def ping():
        return {'message': 'pong'}, 200

    return app

