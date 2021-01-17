import os
from flask import (
    Flask,
    request,
    abort,
    jsonify,
)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, questions: list):
    """
    paginate the question list with pre-defined page limit
    """
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    formatted_questions = [q.format() for q in questions]
    return formatted_questions[start:end]


def create_app(test_config=None):
    """
    create and configure the app
    """
    app = Flask(__name__)
    setup_db(app)

    # Set up CORS. Allow "*" for origins.
    CORS(app)

    # CORS headers
    @app.after_request
    def after_request(response):
        """
        Use the after_request decorator to set Access-Control-Allow
        """
        response.headers.add("Access-Control-Allow-Headers",
                             "Content-Type, Authorization, true")
        response.headers.add("Access-Control-Allow-Methods",
                             "GET, POST, PATCH, DELETE, OPTIONS")
        return response

    @app.route("/categories", methods=['GET'])
    def get_categories():
        """
        endpoint to handle GET requests
        for all available categories.
        """
        categories = Category.query.all()
        formatted_categories = {cat.id: cat.type for cat in categories}

        if len(formatted_categories):
            return jsonify({
                'success': True,
                'categories': formatted_categories,
            })
        else:
            abort(404)

    @app.route("/questions", methods=['GET'])
    def get_questions():
        """
        Create an endpoint to handle GET requests for questions,
        including pagination (every 10 questions).
        This endpoint should return a list of questions,
        number of total questions, current category, categories.

        TEST: At this point, when you start the application
        you should see questions and categories generated,
        ten questions per page and pagination at the bottom of the screen for three pages.
        Clicking on the page numbers should update the questions.
        """
        page = request.args.get('page', 1, type=int)
        questions = Question.query.all()

        if len(questions) == 0 or page > len(questions)//QUESTIONS_PER_PAGE + 1:
            abort(404)
        else:
            questions_onsite = paginate_questions(request, questions)
            categories = {cat.id: cat.type for cat in Category.query.all()}
            return jsonify({
                'success': True,
                'questions': questions_onsite,
                'total_questions': len(questions),
                'current_category': None,
                'categories': categories,
            })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        """
        Create an endpoint to DELETE question using a question ID.

        TEST: When you click the trash icon next to a question, the question will be removed.
        This removal will persist in the database and when you refresh the page.
        """
        try:
            question = Question.query.filter_by(id=question_id).one_or_none()
            question.delete()
            return jsonify({
                'success': True,
                'question_id': question_id,
            })
        except:
            abort(404)

    @app.route('/questions', methods=['POST'])
    def post_question():
        """
        Create an endpoint to POST a new question,
        which will require the question and answer text,
        category, and difficulty score.

        TEST: When you submit a question on the "Add" tab,
        the form will clear and the question will appear at the end of the last page
        of the questions list in the "List" tab.
        """
        body = request.get_json()
        question = Question(
            question=body.get('question'),
            answer=body.get('answer'),
            category=body.get('category'),
            difficulty=body.get('difficulty'),
        )
        if not question.is_valid():
            abort(422)
        try:
            question.insert()
            body['success'] = True
            body['question_id'] = question.id
            return jsonify(body)
        except BaseException as e:
            abort(422)

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        """ 
        Create a POST endpoint to get questions based on a search term.
        It should return any questions for whom the search term
        is a substring of the question.

        TEST: Search by any phrase. The questions list will update to include
        only question that include that string within their question.
        Try using the word "title" to start.
        """
        try:
            search_term = request.get_json().get('searchTerm')
            questions = Question.query.filter(
                Question.question.ilike(f"%{search_term}%")).all()
            if not len(questions):
                abort(404)
            questions_onsite = paginate_questions(request, questions)
            categories = {cat.id: cat.type for cat in Category.query.all()}
            return jsonify({
                'success': True,
                'questions': questions_onsite,
                'found_questions': len(questions),
                'current_category': None,
                'categories': categories,
            })
        except:
            abort(404)

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_in_category(category_id):
        """
        Create a GET endpoint to get questions based on category.

        TEST: In the "List" tab / main screen, clicking on one of the
        categories in the left column will cause only questions of that
        category to be shown.
        """
        cat_ids = Category.query.with_entities(Category.id).all()
        cat_list = [cat for (cat,) in cat_ids]
        if category_id not in cat_list:
            abort(400)
        questions_in_cat = Question.query.filter_by(
            category=category_id).all()
        if not len(questions_in_cat):
            abort(404)
        questions_onsite = paginate_questions(request, questions_in_cat)
        categories = {cat.id: cat.type for cat in Category.query.all()}
        return jsonify({
            'success': True,
            'questions': questions_onsite,
            'found_questions': len(questions_in_cat),
            'current_category': category_id,
            'categories': categories,
        })

    @app.route("/quizzes", methods=['POST'])
    def post_quiz():
        """
        Create a POST endpoint to get questions to play the quiz.
        This endpoint should take category and previous question parameters
        and return a random questions within the given category,
        if provided, and that is not one of the previous questions.

        TEST: In the "Play" tab, after a user selects "All" or a category,
        one question at a time is displayed, the user is allowed to answer
        and shown whether they were correct or not.
        """
        body = request.get_json()
        quiz_cat_id = body.get('quiz_category').get('id')
        previous_qustions = body.get('previous_questions')

        # given a specific category
        if quiz_cat_id:
            questions = Question.query.filter_by(category=quiz_cat_id).filter(Question.id.notin_(previous_qustions)).all()
        # set all categories
        else:
            questions = Question.query.filter(Question.id.notin_(previous_qustions)).all()
        if not questions:
            abort(404)
        
        quiz_question = random.sample(questions, 1)[0].format()
        return jsonify({
            'success': True,
            'question': quiz_question,
        })

    @app.route('/questions/<int:question_id>', methods=['GET'])
    def get_question_with_id(question_id):
        question = Question.query.filter(
            Question.id == question_id).one_or_none()

        if question is None:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'question': question.format(),
            })

    """
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request',
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found',
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable entity',
        }), 422

    return app
