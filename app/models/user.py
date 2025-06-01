"""User model definition."""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.orm import validates
import re

from app.core.extensions import db, login_manager
from app.models.base import BaseModel


class User(BaseModel, UserMixin):
    """User model for authentication and user management."""
    
    __tablename__ = 'users'
    
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    
    # Relacionamentos
    irrigation_controllers = db.relationship(
        'IrrigationController',
        backref=db.backref('owner', lazy='joined'),
        lazy='select',
        cascade='all, delete-orphan'
    )
    
    def __init__(self, username, email, password, first_name=None, last_name=None):
        """Initialize a new user."""
        self.username = username
        self.email = email
        self.set_password(password)
        self.first_name = first_name
        self.last_name = last_name
    
    @validates('username')
    def validate_username(self, key, username):
        """Validate username format and length."""
        if not username:
            raise ValueError('O nome de usuário não pode estar vazio')
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValueError('O nome de usuário deve conter apenas letras, números e underscore')
        if len(username) < 3 or len(username) > 64:
            raise ValueError('O nome de usuário deve ter entre 3 e 64 caracteres')
        return username
    
    @validates('email')
    def validate_email(self, key, email):
        """Validate email format."""
        if not email:
            raise ValueError('O e-mail não pode estar vazio')
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValueError('Formato de e-mail inválido')
        if len(email) > 120:
            raise ValueError('O e-mail deve ter no máximo 120 caracteres')
        return email
    
    def set_password(self, password):
        """Set user password hash."""
        if not password or len(password) < 6:
            raise ValueError('A senha deve ter pelo menos 6 caracteres')
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        """Check if provided password matches user password."""
        return check_password_hash(self.password_hash, password)
    
    @property
    def full_name(self):
        """Get user's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def to_dict(self):
        """Convert user to dictionary representation."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'irrigation_controllers_count': len(self.irrigation_controllers)
        }
    
    def __repr__(self):
        """String representation of user."""
        return f'<User {self.username}>'


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login."""
    return User.query.get(int(user_id)) 