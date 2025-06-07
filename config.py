import os
basedir = os.path.abspath(os.path.dirname(__file__))


# Central place for app configuration
# Reads environment variables (from .env) like DB URI, secret keys, debug flags
# Keeps secrets and settings outside codebase for security and flexibility.
class Config:
    # Get SECRET_KEY from environment variable
    SECRET_KEY = os.getenv('SECRET_KEY')

    # Basic check (optional but good practice)
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set. Please set it in your .env file.")
    
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(basedir, 'schedulingapp.db')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
