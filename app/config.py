'''import os, urllib.parse as up
uri = os.getenv("SQLALCHEMY_DATABASE_URI", "")
if not uri:
    print("Using DB: <not set>")
else:
    p = up.urlparse(uri)
    safe = p._replace(netloc=p.netloc.replace(p.password or "", "***")).geturl()
    print("Using DB:", safe)


class Config: 
    
    
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI= 'postgresql+psycopg2://postgres:dmlaneo4627@db.eggbqllnmdtwvhcaoiva.supabase.co:5432/postgres?sslmode=require&hostaddr=208.67.222.222'



    SQLALCHEMY_TRACK_MODIFICATIONS = False


'''
'''
# app/config.py
import os
from dotenv import load_dotenv, find_dotenv
from sqlalchemy.engine import URL
from sqlalchemy.pool import NullPool  # recommended with PgBouncer

# Load .env once at import time
load_dotenv(find_dotenv(), override=True)

def _build_database_uri() -> str:
    host = os.getenv("DB_HOST")                              # e.g. aws-1-eu-central-1.pooler.supabase.com
    port = int(os.getenv("DB_PORT", "6543"))                 # pooler default
    dbname = os.getenv("DB_NAME", "postgres")
    user = os.getenv("DB_USER")                              # e.g. postgres.eggbqllnmdtwvhcaoiva
    password = os.getenv("DB_PASSWORD")

    if not all([host, user, password]):
        raise RuntimeError("Missing DB env vars. Ensure DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD are set in .env")

    # Build a psycopg2/SQLAlchemy URL; with pooler do NOT set hostaddr
    url = URL.create(
        drivername="postgresql+psycopg2",
        username=user,
        password=password,
        host=host,
        port=port,
        database=dbname,
        query={"sslmode": "require"},
    )
    # Render to full string (Flask-SQLAlchemy expects str)
    return url.render_as_string(hide_password=False)

class Config:
    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(24).hex())

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = _build_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # With PgBouncer (transaction pooler) prefer NO client-side pooling
    SQLALCHEMY_ENGINE_OPTIONS = {
        "poolclass": NullPool,   # avoids “double pooling”
        # If you choose to use client pooling instead, comment the line above and use:
        # "pool_pre_ping": True, "pool_size": 5, "max_overflow": 0,
    }

    # Cookies: reasonable defaults
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
