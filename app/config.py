import os, urllib.parse as up
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


