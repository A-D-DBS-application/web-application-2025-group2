from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
import os

# Load environment
load_dotenv(find_dotenv(), override=True)

host = os.getenv("DB_HOST")
dbname = os.getenv("DB_NAME")
password = os.getenv("DB_PASSWORD")
hostaddr_v6 = os.getenv("DB_HOSTADDR_V6")

print(f"Loaded DB_HOST={host}")
print(f"Loaded DB_NAME={dbname}")
print(f"Password length={len(password) if password else 0}")

# Build SQLAlchemy URL
url = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password=password,
    host=host,
    port=5432,
    database=dbname,
    query={"sslmode": "require", "hostaddr": hostaddr_v6},
)

engine = create_engine(url, pool_pre_ping=True)

# Try connecting
try:
    with engine.connect() as conn:
        ver = conn.execute(text("select version()")).scalar()
        print("✅ Connected successfully!")
        print("Postgres version:", ver)
except Exception as e:
    print("❌ Connection failed:")
    print(e)

