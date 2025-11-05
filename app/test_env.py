from dotenv import load_dotenv
import os
from pathlib import Path

dotenv_path = Path(__file__).resolve().parent / ".env"
print("Looking for:", dotenv_path)
loaded = load_dotenv(dotenv_path, override=True)
print("Loaded:", loaded)

print("DB_PASSWORD =", os.getenv("DB_PASSWORD"))
print("DB_HOST =", os.getenv("DB_HOST"))
print("DB_NAME =", os.getenv("DB_NAME"))
print("DB_HOSTADDR_V6 =", os.getenv("DB_HOSTADDR_V6"))
