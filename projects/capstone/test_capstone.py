import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app, db
from app.models import Vehicle, Client, Booking

ADMIN_TOKEN = f"Bearer {os.environ['ADMIN_TOKEN']}"
USER_TOKEN = f"Bearer {os.environ['USER_TOKEN']}"


class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.admin_header = {'Content-Type': 'application/json',
                             'Authorization': ADMIN_TOKEN}
        self.user_header = {'Content-Type': 'application/json',
                            'Authorization': USER_TOKEN}

        self.valid_vehicle = {
            "make": "Mercedes-Benz",
            "model": "A Class Sedan",
            "model_year": 2015,
            "fuel_type": "petrol",
            "standard_seat_number": 5,
            "automatic": true,
            "bookings_count": 0,
        }

        self.valid_client = {
            "forename": "Alan",
            "surname": "Turing",
            "email": "alan.turing@mustermann.com",
        }

        self.valid_booking = {
            "vehicle_VIN": "11234",
            "client_id": "1912",
            "start_datetime": "2018-08-08T09:00:00.000000",
            "end_datetime": "2018-08-10T21:00:00.000000",
        }

    def tearDown(self):
        """Executed after reach test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_vehicles(self):
        response = self.client().get('/vehicles')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_get_clients(self):
        response = self.client().get('/clients')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_get_bookings(self):
        response = self.client().get('/bookings')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_post_vehicle__missing_header(self):
        res = self.client().post('/vehicles', json=self.valid_vehicle)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_post_vehicle__not_authorized(self):
        res = self.client().post('/vehicles',
                                 json=self.valid_vehicle,
                                 header=self.user_header)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_post_vehicle(self):
        res = self.client().post('/vehicles',
                                 json=self.valid_vehicle,
                                 header=self.admin_header)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_post_client__missing_header(self):
        res = self.client().post('/clients', json=self.valid_client)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_post_client(self):
        res = self.client().post('/clients',
                                 json=self.valid_client,
                                 header=self.admin_header)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_post_client__missing_header(self):
        res = self.client().post('/clients', json=self.valid_booking)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_post_booking(self):
        res = self.client().post('/bookings',
                                 json=self.valid_booking,
                                 header=self.user_header)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_patch_vehicle__missing_header(self):
        res = self.client().patch('/vehicles/1',
                                  json={"model_year": 2018})

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_patch_vehicle__not_authorized(self):
        res = self.client().patch('/vehicles/1',
                                  json={"model_year": 2018},
                                  header=self.user_header)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_patch_vehicle(self):
        res = self.client().patch('/vehicles/1',
                                  json={"model_year": 2018},
                                  header=self.admin_header)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_patch_client__missing_header(self):
        res = self.client().patch('/clients', json=self.valid_client)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_patch_client(self):
        res = self.client().patch('/clients/1',
                                  json={"forename": "Alen"},
                                  header=self.admin_header)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_patch_client__missing_header(self):
        res = self.client().patch('/clients/1',
                                  json={
                                      "start_datetime": "2018-08-09T09:00:00.000000"
                                  })

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_patch_booking(self):
        res = self.client().patch('/bookings/1',
                                  json={
                                      "start_datetime": "2018-08-09T09:00:00.000000"},
                                  header=self.user_header)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_delete_vehicle__missing_header(self):
        res = self.client().delete('/vehicles/1')

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_delete_vehicle__not_authorized(self):
        res = self.client().delete('/vehicles/1', header=self.user_header)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_delete_vehicle(self):
        res = self.client().delete('/vehicles/1', header=self.admin_header)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_delete_client__missing_header(self):
        res = self.client().delete('/clients')

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_delete_client(self):
        res = self.client().delete('/clients/1', header=self.admin_header)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_delete_client__missing_header(self):
        res = self.client().delete('/clients/1')

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_delete_booking(self):
        res = self.client().delete('/bookings/1', header=self.user_header)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
