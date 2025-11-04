from flask import Flask
from .models import db
from .config import Config

'''def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()  # Create sql tables for our data models

    from .routes import main
    app.register_blueprint(main)

    return app
'''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import URL
from sqlalchemy import create_engine, text
from dotenv import load_dotenv, find_dotenv
import os

# ✅ Load environment variables reliably
load_dotenv(find_dotenv(), override=True)

# Initialize SQLAlchemy
db = SQLAlchemy()

def create_app():
    # Read env vars
    host = os.getenv("DB_HOST", "db.eggbqllnmdtwvhcaoiva.supabase.co")
    dbname = os.getenv("DB_NAME", "postgres")
    password = os.getenv("DB_PASSWORD")
    hostaddr_v6 = os.getenv("DB_HOSTADDR_V6")

    # Debug info
    print(f"DB config -> host={host} db={dbname} user=postgres pw_len={0 if password is None else len(password)} v6={hostaddr_v6}")

    if not password:
        raise RuntimeError("❌ DB_PASSWORD not set — check your .env file")

    # Build SQLAlchemy URL
    db_url = URL.create(
        drivername="postgresql+psycopg2",
        username="postgres",
        password=password,  # include password securely
        host=host,
        port=5432,
        database=dbname,
        query={
            "sslmode": "require",
            "hostaddr": hostaddr_v6
        },
    )

    # ✅ Preflight test — same as test_db.py
    try:
        engine_probe = create_engine(db_url, pool_pre_ping=True)
        with engine_probe.connect() as conn:
            ver = conn.execute(text("select version()")).scalar()
            print("✅ Preflight DB connect OK. Server version:", ver)
    except Exception as e:
        print("❌ Preflight DB connect FAILED. Check your .env credentials.")
        print(e)
        raise

    # ✅ Render URL correctly with password visible (don’t use str(db_url))
    uri = db_url.render_as_string(hide_password=False)

    # Flask app setup
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize SQLAlchemy with app
    db.init_app(app)

    # Create tables (if needed)
    with app.app_context():
        db.create_all()

    print("✅ Flask app configured and DB tables ensured.")
    return app
