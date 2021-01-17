import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app, QUESTIONS_PER_PAGE
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            'postgres', 'postgres', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.valid_question = {
            "question": "Who invented the automobile?",
            "answer": "Karl Benz",
            "category": 4,
            "difficulty": 2,
        }

        self.invalid_question = {
            "question": "How are you?",
            "answer": "",
            "category": 1,
            "difficulty": None,
        }

        self.quiz_info_all_categories = {
            'quiz_category': {
                'type': 'click',
                'id': 0,
            },
            "previous_questions": [],
        }

        self.quiz_info_specific_category = {
            'quiz_category': {
                'type': 'Science',
                'id': 1,
            },
            "previous_questions": [],
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
        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['questions']), 9)
        self.assertEqual(data['total_questions'], 19)
        self.assertIsNone(data['current_category'])
        self.assertEqual(len(data['categories']), 6)

    def test_404_sent_requsting_beyond_valid_page(self):
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')

    def test_post_valid_question(self):
        res = self.client().post('/questions', json=self.valid_question)
        data = json.loads(res.data)
        question = Question.query.filter_by(
            id=data['question_id']).one_or_none()
        formated_question = question.format()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(
            formated_question['question'], self.valid_question['question'])
        self.assertTrue(
            formated_question['answer'], self.valid_question['answer'])
        self.assertTrue(
            formated_question['category'], self.valid_question['category'])
        self.assertTrue(
            formated_question['difficulty'], self.valid_question['difficulty'])

        # delete the record after execution
        question.delete()

    def test_422_post_invalid_question(self):
        res = self.client().post('/questions', json=self.invalid_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable entity')

    def test_delete_question(self):
        # insert a new record before execution
        question = Question(
            question=self.valid_question['question'],
            answer=self.valid_question['answer'],
            category=self.valid_question['category'],
            difficulty=self.valid_question['difficulty'])
        question.insert()

        res = self.client().delete(f'/questions/{str(question.id)}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['question_id'], question.id)

    def test_404_delete_non_existing_question(self):
        res = self.client().delete(f'/questions/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')

    def test_search_question(self):
        res = self.client().post('/questions/search',
                                 json={'searchTerm': 'World Cup'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['found_questions'], 2)

    def test_404_search_question_non_existing_term(self):
        res = self.client().post('/questions/search',
                                 json={'searchTerm': 'NON EXISTING'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')

    def test_search_questions_in_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['current_category'], 1)
        self.assertEqual(data['found_questions'], 3)

    def test_400_search_questions_in_non_existing_category(self):
        res = self.client().get('/categories/100/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'bad request')

    def test_404_search_questions_in_empty_categort(self):
        category = Category(type='test')
        category.insert()
        res = self.client().get(f"/categories/{str(category.id)}/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')

        category.delete()

    def test_post_quiz_all_categories(self):
        res = self.client().post('/quizzes', json=self.quiz_info_all_categories)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['question'])

    def test_post_quiz_specific_category(self):
        res = self.client().post('/quizzes', json=self.quiz_info_specific_category)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(
            data['question']['id'], self.quiz_info_specific_category['quiz_category']['id'])

    def test_404_post_quiz_no_questions_left(self):
        quiz_info = self.quiz_info_all_categories
        question_ids = Question.query.with_entities(Question.id).all()
        question_list = [q for (q,) in question_ids]
        quiz_info['previous_questions'] = question_list
        res = self.client().post('/quizzes', json=quiz_info)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
