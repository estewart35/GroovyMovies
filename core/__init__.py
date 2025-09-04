# core/__init__.py
from flask import Flask
from core import models
from core.extensions import db, login_manager, migrate
from core.routes.web import web
from datetime import timedelta
from sqlalchemy.exc import OperationalError
from sqlalchemy import text
import os, time

def wake_db(app, retries=5, delay=2):
    """Attempt to wake up the DB on app startup."""
    with app.app_context():
        for i in range(retries):
            try:
                db.session.execute(text("SELECT 1"))
                print("✅ Database awake!")
                return
            except OperationalError:
                print(f"⏳ Waiting for DB... attempt {i+1}/{retries}")
                time.sleep(delay)
        print("❌ Could not connect to DB after retries")


def create_app(environment="production"):
    app = Flask(__name__)

    # Load configurations based on the environment
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["DEBUG"] = environment == "development"
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    # Initialize extensions
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # Initialize migrations
    migrate.init_app(app, db)

    from core.routes.auth import auth
    from core.routes.web import web

    # Register blueprints
    app.register_blueprint(auth)
    app.register_blueprint(web)

    # Wake up DB immediately on app startup
    wake_db(app)

    return app
