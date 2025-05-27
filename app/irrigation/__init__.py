"""Irrigation module initialization."""

from flask import Blueprint

irrigation = Blueprint('irrigation', __name__, url_prefix='/irrigation')

from . import routes 