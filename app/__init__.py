import os

from flask import Flask
from config import Config
from app.extensions import db, login_manager, migrate, csrf


def create_app():

    app = Flask(
        __name__,
        instance_relative_config=True
    )

    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # Login configuration
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please login to continue."
    login_manager.login_message_category = "info"

    # Create instance folder
    os.makedirs(app.instance_path, exist_ok=True)

    # Import database models
    from app import models

    # Import blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.products import products_bp
    from app.routes.cart import cart_bp
    from app.routes.orders import orders_bp

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(orders_bp)

    return app
