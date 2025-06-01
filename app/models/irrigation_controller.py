"""Irrigation Controller model definition."""

from datetime import datetime
from sqlalchemy.orm import validates

from app.core.extensions import db
from app.models.base import BaseModel


class IrrigationController(BaseModel):
    """Irrigation Controller model for managing irrigation systems."""
    
    __tablename__ = 'irrigation_controllers'
    
    name = db.Column(db.String(100), nullable=False)
    moisture_level = db.Column(db.Float, nullable=False, default=0.0)
    last_irrigation = db.Column(db.DateTime, nullable=True)
    
    # Configurações do controlador
    min_moisture_threshold = db.Column(db.Float, nullable=False, default=30.0)
    max_moisture_threshold = db.Column(db.Float, nullable=False, default=80.0)
    irrigation_duration = db.Column(db.Integer, nullable=False, default=300)  # em segundos
    
    # Relacionamento com usuário
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    def __init__(self, name, user_id, moisture_level=0.0, min_moisture_threshold=30.0,
                 max_moisture_threshold=80.0, irrigation_duration=300):
        """Initialize a new irrigation controller."""
        self.name = name
        self.user_id = user_id
        self.moisture_level = moisture_level
        self.min_moisture_threshold = min_moisture_threshold
        self.max_moisture_threshold = max_moisture_threshold
        self.irrigation_duration = irrigation_duration
    
    @validates('name')
    def validate_name(self, key, name):
        """Validate controller name."""
        if not name:
            raise ValueError('O nome do controlador não pode estar vazio')
        if len(name) > 100:
            raise ValueError('O nome do controlador deve ter no máximo 100 caracteres')
        return name
    
    @validates('moisture_level', 'min_moisture_threshold', 'max_moisture_threshold')
    def validate_moisture_values(self, key, value):
        """Validate moisture related values."""
        if value < 0.0 or value > 100.0:
            raise ValueError(f'O valor de {key} deve estar entre 0 e 100')
        return value
    
    @validates('irrigation_duration')
    def validate_irrigation_duration(self, key, value):
        """Validate irrigation duration."""
        if value < 0:
            raise ValueError('A duração da irrigação não pode ser negativa')
        if value > 3600:  # máximo 1 hora
            raise ValueError('A duração da irrigação não pode ser maior que 1 hora')
        return value
    
    def update_moisture_level(self, level):
        """Update the moisture level."""
        self.moisture_level = level
        self.updated_at = datetime.utcnow()
        self.save()
    
    def irrigate(self):
        """Mark the controller as irrigated."""
        self.last_irrigation = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.save()
    
    @property
    def needs_irrigation(self):
        """Check if irrigation is needed based on moisture level."""
        return self.moisture_level < self.min_moisture_threshold
    
    @property
    def status(self):
        """Get the current status of the controller."""
        if not self.is_active:
            return 'inativo'
        elif self.needs_irrigation:
            return 'necessita_irrigacao'
        elif self.moisture_level > self.max_moisture_threshold:
            return 'muito_umido'
        else:
            return 'ok'
    
    def to_dict(self):
        """Convert irrigation controller to dictionary representation."""
        return {
            'id': self.id,
            'name': self.name,
            'moisture_level': self.moisture_level,
            'min_moisture_threshold': self.min_moisture_threshold,
            'max_moisture_threshold': self.max_moisture_threshold,
            'irrigation_duration': self.irrigation_duration,
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