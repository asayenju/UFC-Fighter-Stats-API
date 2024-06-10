from flask import Flask
from api.routes import fighters

app = Flask(__name__)

#Register blueprint for fighters routes
app.register_blueprint(fighters.bp)

if __name__ == '__main__':
    app.run(debug=True)