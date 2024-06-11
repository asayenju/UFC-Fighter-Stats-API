from flask import Flask
import os
import sys

# Append the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api.routes import fighters

app = Flask(__name__)

#Register blueprint for fighters routes
app.register_blueprint(fighters.bp)

if __name__ == '__main__':
    app.run(debug=True)