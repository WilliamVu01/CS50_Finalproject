# Finalproject/config.py

import os

# Get the base directory of the project
basedir = os.path.abspath(os.path.dirname(__file__))

# Central place for app configuration
# This 'Config' class holds common configurations for all environments.
class Config:
    # Get SECRET_KEY from environment variable
    SECRET_KEY = os.getenv('SECRET_KEY')

    # Basic check (optional but good practice)
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set. Please set it in your .env file.")

    # Database URI for SQLAlchemy. Uses DATABASE_URL from .env or defaults to SQLite.
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(basedir, 'schedulingapp.db')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Disable Flask-SQLAlchemy event system overhead

# Development-specific configurations
# This class inherits from Config, so it gets all base settings,
# and you can override or add development-specific ones here.
class DevelopmentConfig(Config):
    DEBUG = True # Enable Flask debug mode
    # You might override database URL or other settings here if needed for dev
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URL", f"sqlite:///{os.path.join(basedir, 'dev_schedulingapp.db')}")

# Testing-specific configurations
# This class would be used for running automated tests.
class TestingConfig(Config):
    TESTING = True # Enable Flask testing mode
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:" # Use an in-memory SQLite database for tests
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 4 # Faster bcrypt for tests

# Production-specific configurations
# This class would contain settings optimized for a live environment.
class ProductionConfig(Config):
    DEBUG = False # Disable debug mode in production
    # SQLALCHEMY_DATABASE_URI = os.getenv("PROD_DATABASE_URL") # Use a robust production database
    # Other production specific settings like logging, error reporting etc.