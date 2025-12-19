from app import create_app
import os

app = create_app()

if __name__ == "__main__":
    # Use PORT env var if present (useful for hosting), default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Disable debug mode for production
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
