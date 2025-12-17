# app/__init__.py
from flask import Flask
from app.models import db  # Import db from models


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    db.init_app(app)

    from app.constants import APP_NAME
    from app.routes import main, dashboard, bookings
    app.register_blueprint(main)
    app.register_blueprint(dashboard)
    app.register_blueprint(bookings)

    with app.app_context():
        db.create_all()


        @app.context_processor
        def inject_app_name():
            return dict(app_name=APP_NAME)
    # Hier kan je de naam van de app centraal aanpassen zodanig dat de naam niet hard gecodeerd is

    return app
