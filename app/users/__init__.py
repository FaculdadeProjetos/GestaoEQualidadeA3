"""Users module initialization."""

from flask import Blueprint

users = Blueprint('users', __name__, url_prefix='/users')

from . import routes   # Importa as rotas para ativar no app