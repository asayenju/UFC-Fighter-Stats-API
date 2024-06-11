import os
import sys

# Prevent the creation of .pyc files and __pycache__ directories
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

# Append the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from routes.fighters import app as fighters_app

# Use the routes defined in fighters.py
app = fighters_app

if __name__ == '__main__':
    app.run(debug=True)