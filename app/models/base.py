"""Base model with common functionality."""

from datetime import datetime
from app.core.extensions import db


class BaseModel(db.Model):
    """Base model class with common attributes and methods."""
    
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    def save(self):
        """Save the model instance to the database."""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    def delete(self):
        """Delete the model instance from the database."""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    def soft_delete(self):
        """Soft delete the model instance by setting is_active to False."""
        try:
            self.is_active = False
            self.save()
            return True
        except Exception as e:
            db.session.rollback()
            raise e 