from app.models import User
from app.core.extensions import db
from sqlalchemy.exc import IntegrityError

def create_user(data):
    user = User(
        username=data['username'],
        email=data['email'],
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        is_active=data.get('is_active', True)
    )
    if data.get('password'):
        user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()
    return user

def update_user(user, data):
    user.username = data['username']
    user.email = data['email']
    user.first_name = data.get('first_name')
    user.last_name = data.get('last_name')
    user.is_active = data.get('is_active', True)

    if data.get('password'):
        user.set_password(data['password'])

    db.session.commit()
    return user

def delete_user(user):
    db.session.delete(user)
    db.session.commit()
