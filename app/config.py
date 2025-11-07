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

# app/config.py
import os
from dotenv import load_dotenv, find_dotenv
from sqlalchemy.engine import URL

# Load .env once at import time
load_dotenv(find_dotenv(), override=True)

def _build_database_uri() -> str:
    host = os.getenv("DB_HOST", "db.eggbqllnmdtwvhcaoiva.supabase.co")
    port = int(os.getenv("DB_PORT", "5432"))
    dbname = os.getenv("DB_NAME", "postgres")
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD")

    if not password:
        raise RuntimeError("DB_PASSWORD is not set. Create a .env file with DB_* values.")

    # Prefer IPv4 hostaddr if provided; else IPv6; else rely on DNS
    v4 = os.getenv("DB_HOSTADDR_V4")
    v6 = os.getenv("DB_HOSTADDR_V6")
    query = {"sslmode": "require"}
    if v4:
        query["hostaddr"] = v4
    elif v6:
        query["hostaddr"] = v6

    url = URL.create(
        drivername="postgresql+psycopg2",
        username=user,
        password=password,
        host=host,            # keep hostname for TLS/SNI
        port=port,
        database=dbname,
        query=query,
    )

    # IMPORTANT: Flask-SQLAlchemy expects a full string; render with password visible
    return url.render_as_string(hide_password=False)

class Config:
    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(24).hex())

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = _build_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,   # avoid stale connections
    }

    # Session cookie hardening (safe defaults)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
