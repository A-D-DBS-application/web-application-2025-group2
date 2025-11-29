# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.models import db
    db.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    return app
