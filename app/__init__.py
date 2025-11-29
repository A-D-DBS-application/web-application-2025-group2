# app/__init__.py
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS for React frontend
    CORS(app, origins=["http://localhost:5173"], supports_credentials=True)

    from app.models import db
    db.init_app(app)

    from app.routes import main
    app.register_blueprint(main, url_prefix='/api')  # All routes under /api

    return app
