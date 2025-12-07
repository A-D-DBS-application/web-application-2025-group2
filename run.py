from app import create_app
import os

app = create_app()

<<<<<<< HEAD
if __name__ == "__main__":
    # Use PORT env var if present (useful for hosting), default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
=======
if __name__ == '__main__':
    app.run(debug=True)
>>>>>>> 6cdc61bcf744dc751babcbf5016d05c0c31e8632
