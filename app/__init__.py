from flask import Flask 
from .routes import app as main_blueprint

def create_app():
    app = Flask(__name__)

    app.register_blueprint(app)

    return app