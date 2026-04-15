import os
import logging
from logging import FileHandler, Formatter
from flask import Flask
from flask_migrate import Migrate
from config import Config
from .extensions import db, migrate
from .routes import main_bp

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(main_bp)

    log_dir = "/var/log/flask"
    os.makedirs(log_dir, exist_ok=True)

    auth_handler = FileHandler(f"{log_dir}/auth.log")
    auth_handler.setLevel(logging.INFO)
    auth_handler.setFormatter(Formatter(
        "%(asctime)s %(levelname)s %(message)s"
    ))

    auth_logger = logging.getLogger("auth_logger")
    auth_logger.setLevel(logging.INFO)
    if not auth_logger.handlers:
    	auth_logger.addHandler(auth_handler)
    auth_logger.propagate = False

    app.auth_logger = auth_logger

    return app
