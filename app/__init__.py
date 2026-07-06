"""
MindTrack — Mental Health & Wellness Tracker (SDG 3: Good Health and Well-being)

Application factory for the Flask app.
"""
from flask import Flask
from app.db import init_db


def create_app():
    app = Flask(__name__)
    app.config["DATABASE"] = "data/mindtrack.db"

    with app.app_context():
        init_db(app.config["DATABASE"])

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app
