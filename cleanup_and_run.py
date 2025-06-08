#!/usr/bin/env python3
# Finalproject/cleanup_and_run.py

import os
import shutil
import subprocess
import sys

# Define the root directory of your project
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

def clear_pycache():
    """Recursively deletes all __pycache__ directories and .pyc files."""
    print("--- Clearing Python bytecode cache (recursively deleting __pycache__ and .pyc files) ---")
    for root, dirs, files in os.walk(PROJECT_ROOT):
        if "__pycache__" in dirs:
            cache_path = os.path.join(root, "__pycache__")
            print(f"Deleting: {cache_path}")
            shutil.rmtree(cache_path)
        for f in files:
            if f.endswith(".pyc"):
                pyc_path = os.path.join(root, f)
                print(f"Deleting: {pyc_path}")
                os.remove(pyc_path)
    print("--- Cache cleared successfully ---")

def deactivate_venv():
    """Attempts to deactivate the virtual environment."""
    print("--- Attempting to deactivate virtual environment ---")
    # This is tricky in a script, as 'deactivate' is a shell function.
    # We'll just rely on the subprocess call below to use the correct venv python.
    # For a clean shell prompt, manual `deactivate` is best.
    pass # No direct way to deactivate parent shell from a script

def activate_and_run():
    """Activates venv and runs the Flask app."""
    print("--- Activating virtual environment and running Flask app ---")
    venv_python = os.path.join(PROJECT_ROOT, 'venv', 'bin', 'python')
    if sys.platform == "win32":
        venv_python = os.path.join(PROJECT_ROOT, 'venv', 'Scripts', 'python.exe')

    if not os.path.exists(venv_python):
        print(f"Error: Virtual environment Python executable not found at {venv_python}")
        print("Please ensure your virtual environment is set up correctly.")
        sys.exit(1)

    # Use the venv's python to run run.py
    try:
        # Use subprocess.run with check=True to raise an exception on non-zero exit codes
        # This will stream output directly to the console
        subprocess.run([venv_python, os.path.join(PROJECT_ROOT, 'run.py')], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Flask application exited with an error: {e}")
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        print("\nFlask server stopped by user.")

if __name__ == "__main__":
    clear_pycache()
    # No direct deactivate here, but subsequent calls ensure venv's python is used
    activate_and_run()
