
"""
WSGI entry point for production servers (Gunicorn, Render, etc.).
 
run.py uses Flask's dev server (app.run) which isn't meant for real
traffic. This file exposes the actual `app` object that Gunicorn
can import and serve.
"""
from app import create_app
 
app = create_app()
 