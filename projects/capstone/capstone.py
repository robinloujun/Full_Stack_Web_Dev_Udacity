import os
import sys
import click
from flask_migrate import Migrate, upgrade
from app import create_app, db
from app.models import Vehicle, Client, Booking

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
