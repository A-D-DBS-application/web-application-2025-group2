from app import create_app, db
from sqlalchemy import text

app = create_app()
with app.app_context():
    with db.engine.connect() as conn:
        conn.execute(text('ALTER TABLE photo ALTER COLUMN image_url TYPE TEXT;'))
        conn.commit()
    print('Column type updated successfully! You can now upload photos.')
