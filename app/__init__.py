import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize SQLAlchemy
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-dev-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    with app.app_context():
        # Import parts of our application
        from app.models import User, IrrigationController
        from app.auth import auth as auth_blueprint
        from app.users import users as users_blueprint
        from app.irrigation import irrigation as irrigation_blueprint
        
        # Register blueprints
        app.register_blueprint(auth_blueprint)
        app.register_blueprint(users_blueprint)
        app.register_blueprint(irrigation_blueprint)
        
        # Create database tables
        db.create_all()
        
        return app 