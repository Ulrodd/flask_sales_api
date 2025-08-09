from flask import Flask
from .db import init_db
from .routes import api_bp

def create_app():
    app = Flask(__name__)
    init_db()
    app.register_blueprint(api_bp)
    return app
