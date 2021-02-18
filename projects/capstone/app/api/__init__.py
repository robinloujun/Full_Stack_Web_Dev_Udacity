from . import authentication, vehicles, clients, bookings, errors
from flask import Blueprint

api = Blueprint('api', __name__)
