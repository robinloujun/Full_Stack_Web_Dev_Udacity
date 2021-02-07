import os
import sys
import click
from flask_migrate import Migrate, upgrade
from app import create_app, db
# from app.models import User, Follow, Role, Permission, Post, Comment

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)