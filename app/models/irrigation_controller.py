"""Irrigation Controller model definition."""

from datetime import datetime
from app.core.extensions import db


class IrrigationController(db.Model):
    """Irrigation Controller model for managing irrigation systems."""
    
    __tablename__ = 'irrigation_controllers'
    
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(100), nullable=False)
    moisture_level = db.Column(db.Float, nullable=False, default=0.0)
    last_irrigation = db.Column(db.DateTime, nullable=True)
    
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    user = db.relationship('User', backref=db.backref('irrigation_controllers', lazy=True))
    
    def __init__(self, name, user_id, moisture_level=0.0):
        """Initialize a new irrigation controller."""
        self.name = name
        self.user_id = user_id
        self.moisture_level = moisture_level
    
    def update_moisture_level(self, level):
        """Update the moisture level."""
        self.moisture_level = level
        self.updated_at = datetime.utcnow()
    
    def irrigate(self):
        """Mark the controller as irrigated."""
        self.last_irrigation = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    @property
    def needs_irrigation(self):
        """Check if irrigation is needed based on moisture level."""
        return self.moisture_level < 30.0
    
    @property
    def status(self):
        """Get the current status of the controller."""
        if not self.is_active:
            return 'inactive'
        elif self.needs_irrigation:
            return 'needs_irrigation'
        else:
            return 'ok'
    
    def to_dict(self):
        """Convert irrigation controller to dictionary representation."""
        return {
            'id': self.id,
            'name': self.name,
            'moisture_level': self.moisture_level,
            'last_irrigation': self.last_irrigation.isoformat() if self.last_irrigation else None,
            'is_active': self.is_active,
            'needs_irrigation': self.needs_irrigation,
            'status': self.status,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        """String representation of irrigation controller."""
        return f'<IrrigationController {self.name}>' 