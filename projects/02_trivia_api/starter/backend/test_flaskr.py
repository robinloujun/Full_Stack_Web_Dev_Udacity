import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(
            'postgres', 'postgres', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_category = {
            "id": 1,
            "type": "Science",
        }

        self.new_question = {
            "id": 1,
            "question": "Who discovered penicillin?",
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['categories']), 6)

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['questions']), 10)
        self.assertEqual(data['total_questions'], 19)

    def test_404_sent_requsting_beyond_valid_page(self):
        res = self.client().get('/questions?page=100', json={'difficulty': 1})
        data = json.loads(res.data)
        print(data)
        print('code', res.status_code)

        self.assertEqual(res.status_code, 404)
        self.assertTrue(data['success'], False)
        self.assertEqual(len(data['questions']), 10)
        self.assertEqual(data['total_questions'], 19)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
