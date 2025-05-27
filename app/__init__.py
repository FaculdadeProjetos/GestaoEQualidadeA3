"""Flask application factory."""

import os
from flask import Flask

from config import config
from app.core.extensions import init_extensions, db


def create_app(config_name=None):
    """Create and configure Flask application.
    
    Args:
        config_name (str): Configuration name ('development', 'production', 'testing')
        
    Returns:
        Flask: Configured Flask application instance
    """
    # Determine configuration
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    init_extensions(app)
    
    # Register blueprints
    _register_blueprints(app)
    
    # Create database tables
    _create_tables(app)
    
    return app


def _register_blueprints(app):
    """Register application blueprints.
    
    Args:
        app (Flask): Flask application instance
    """
    from app.auth import auth as auth_blueprint
    from app.users import users as users_blueprint
    from app.irrigation import irrigation as irrigation_blueprint
    
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(users_blueprint)
    app.register_blueprint(irrigation_blueprint)


def _create_tables(app):
    """Create database tables.
    
    Args:
        app (Flask): Flask application instance
    """
    with app.app_context():
        # Import models to ensure they are registered
        from app.models import User, IrrigationController
        
        # Create all tables
        db.create_all() 