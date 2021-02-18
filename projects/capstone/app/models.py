import json
from markdown import markdown
from datetime import datetime
from . import db
from flask_login import UserMixin, AnonymousUserMixin

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Vehicle(db.Model):
    __tablename__ = "vehicles"

    VIN = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(64))
    model = db.Column(db.String(64))
    model_year = db.Column(db.Integer)
    fuel_type = db.Column(db.String(64))
    standard_seat_number = db.Column(db.Integer)
    automatic = db.Column(db.Boolean)
    bookings = db.relationship("Booking", backref="vehicles")


class Client(db.Model):
    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True)
    forename = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True, index=True)
    bookings = db.relationship("Booking", backref="clients")


class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    vehicle_VIN = db.Column(db.Integer, db.ForeignKey("vehicles.VIN"))
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"))
    start_datetime = db.Column(db.DateTime, nullable=False)
    end_datetime = db.Column(db.DateTime, nullable=False)
    vehicle = db.relationship("Vehicle")
    client = db.relationship("Client")
