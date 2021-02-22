import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app, db
from app.models import Vehicle, Client, Booking


class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_vehicles(self):
        pass


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
