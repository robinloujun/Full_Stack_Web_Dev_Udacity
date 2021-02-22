import os
import json
from datetime import datetime
from . import db


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

    def to_json(self):
        return {
            "VIN": self.VIN,
            "make": self.make,
            "model": self.model,
            "model_year": self.model_year,
            "fuel_type": self.fuel_type,
            "standard_seat_number": self.standard_seat_number,
            "automatic": self.automatic,
            "bookings_count": self.bookings.count(),
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.to_json())


class Client(db.Model):
    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True)
    forename = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True, index=True)
    bookings = db.relationship("Booking", backref="clients")

    def to_json(self):
        return {
            "id": self.id,
            "client_uuid": self.client_uuid,
            "forename": self.forename,
            "surname": self.surname,
            "email": self.email,
            "bookings_count": self.bookings.count(),
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.to_json())


class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    vehicle_VIN = db.Column(db.Integer, db.ForeignKey("vehicles.VIN"))
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"))
    start_datetime = db.Column(db.DateTime, nullable=False)
    end_datetime = db.Column(db.DateTime, nullable=False)
    vehicle = db.relationship("Vehicle")
    client = db.relationship("Client")

    def to_json(self):
        return {
            "id": self.id,
            "vehicle_VIN": self.vehicle_VIN,
            "client_id": self.client_id,
            "start_datetime": self.start_datetime,
            "end_datetime": self.end_datetime,
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.to_json())
