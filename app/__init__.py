from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    load_dotenv()  # load .env file

    app = Flask(__name__)
    app.config.from_object('config.Config')  # load config from config.py

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Import and register blueprints here (later)

    @app.route('/ping')
    def ping():
        return {'message': 'pong'}, 200

    return app
