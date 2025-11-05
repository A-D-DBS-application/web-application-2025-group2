import os
from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from dotenv import load_dotenv

db = SQLAlchemy()

def create_app():
    # ---- Load .env from project root (next to run.py) ----
    dotenv_path = Path(__file__).resolve().parents[1] / ".env"
    loaded = load_dotenv(dotenv_path, override=True)
    print(f"[dotenv] path={dotenv_path} exists={dotenv_path.exists()} loaded={loaded}")

    # ---- Read env vars ----
    host = os.getenv("DB_HOST", "db.eggbqllnmdtwvhcaoiva.supabase.co")
    dbname = os.getenv("DB_NAME", "postgres")
    password = os.getenv("DB_PASSWORD")
    hostaddr_v6 = os.getenv("DB_HOSTADDR_V6")

    print(f"DB config -> host={host} db={dbname} user=postgres pw_len={0 if password is None else len(password)} v6={hostaddr_v6}")
    if not password:
        raise RuntimeError("❌ DB_PASSWORD not set — check your .env file location/content")

    # ---- Build URL ----
    db_url = URL.create(
        drivername="postgresql+psycopg2",
        username="postgres",
        password=password,
        host=host,
        port=5432,
        database=dbname,
        query={"sslmode": "require", "hostaddr": hostaddr_v6},
    )

    # ---- Preflight connect ----
    engine_probe = create_engine(db_url, pool_pre_ping=True)
    with engine_probe.connect() as conn:
        ver = conn.execute(text("select version()")).scalar()
        print("✅ Preflight DB connect OK. Server version:", ver)

    # ---- Configure Flask ----
    uri = db_url.render_as_string(hide_password=False)
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    @app.get("/")
    def home():
        return "<h1>✅ Flask app is running!</h1><p>Connected to Supabase successfully.</p>"

    @app.get("/healthz")
    def healthz():
        return {"status": "ok"}

    db.init_app(app)
    with app.app_context():
        db.create_all()

    print("✅ Flask app configured and DB tables ensured.")
    return app







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
