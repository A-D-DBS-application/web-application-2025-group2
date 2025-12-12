from flask import Flask
from flask_sqlalchemy import SQLAlchemy
 
print("--- Starting Sanity Check ---")
 
app = Flask(__name__)
 
# Define the URL as a variable
db_url = "postgresql://postgres.eggbqllnmdtwvhcaoiva:rpsxmeo8912@aws-0-eu-central-1.pooler.supabase.com:6543/postgres"
 
print(f"The database URL is: {db_url}")
print(f"Is the URL None? {'Yes' if db_url is None else 'No'}")
 
# Configure the app
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
print("Initializing database...")
 
try:
    # This is where the error happens
    db = SQLAlchemy(app)
    print("--- SUCCESS: Database initialized without error. ---")
except Exception as e:
    print(f"--- ERROR: An error occurred: {e} ---")
 
print("--- Sanity Check Finished ---")