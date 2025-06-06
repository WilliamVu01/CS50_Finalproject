import os


# Central place for app configuration
# Reads environment variables (from .env) like DB URI, secret keys, debug flags
# Keeps secrets and settings outside codebase for security and flexibility.
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///schedulingapp.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-key")
