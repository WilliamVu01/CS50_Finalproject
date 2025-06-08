# Finalproject/app/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

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

login_manager = LoginManager()

# the tools for handling password hash and check passwords
# Initialize here for connect to app
bcrypt = Bcrypt()