"""Application entry point for WSGI server and local development.

Note: Port 80 is used locally. For 0.0.0.0 binding in production,
use a WSGI server like Gunicorn.
"""
import os
from dashboard import create_app

app = create_app()

if __name__ == "__main__":
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 80))
    app.run(host=host, port=port)