import pytest
import os
import sys
# Append the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api.app import app as flask_app

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True

    with flask_app.test_client() as client:
        with flask_app.app_context():
            yield client