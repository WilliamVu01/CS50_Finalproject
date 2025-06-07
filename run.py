from app import create_app

# Entry point script to start the Flask development server
# Imports app from app/__init__.py and runs it.
# Keeps the server startup logic separate from my app logic

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
