import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

"""
initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
"""
db_drop_and_create_all()

# ROUTES


@app.route('/drinks', methods=['GET'])
def get_drinks():
    """
    public endpoint GET /drinks
    contains only the drink.short() data representation
    Returns:
        status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        appropriate status code indicating reason for failure
    """
    try:
        drinks = [drink.short() for drink in Drink.query.all()]
        return jsonify({
            'success': True,
            'drinks': drinks,
        })
    except:
        abort(500)


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    """
    endpoint GET /drinks-detail
    requires the 'get:drinks-detail' permission
    contains the drink.long() data representation
    Returns:
        status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        appropriate status code indicating reason for failure
    """
    try:
        drinks = [drink.long() for drink in Drink.query.all()]
        return jsonify({
            'success': True,
            'drinks': drinks,
        })
    except:
        abort(500)


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drink(payload):
    """
    endpoint POST /drinks
    creates a new row in the drinks table
    requires the 'post:drinks' permission
    contains the drink.long() data representation
    Returns:
        status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        appropriate status code indicating reason for failure
    """
    body = request.get_json()

    drink = Drink(
        title=body.get('title'),
        recipe=json.dumps(body.get('recipe')),
    )
    try:
        drink.insert()
        return jsonify({
            'success': True,
            'drinks': [drink.long()],
        })
    except:
        abort(422)


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drink(payload, id):
    """
    endpoint PATCH /drinks/<id>, where <id> is the existing model id
    responds with a 404 error if <id> is not found
    updates the corresponding row for <id>
    requires the 'patch:drinks' permission
    contains the drink.long() data representation
    Returns:
        status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        appropriate status code indicating reason for failure
    """
    try:
        body = request.get_json()
        drink = Drink.query.filter_by(id=id).one_or_none()
        if drink:
            if 'title' in body:
                drink.title = body.get('title')
            if 'recipe' in body:
                drink.recipe = json.dumps(body.get('recipe'))
            drink.update()
            return jsonify({
                'success': True,
                'drinks': [drink.long()],
            })
        else:
            abort(404)
    except:
        abort(500)


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    """
    endpoint DELETE /drinks/<id>, where <id> is the existing model id
    responds with a 404 error if <id> is not found
    deletes the corresponding row for <id>
    requires the 'delete:drinks' permission
    Returns:
        status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        appropriate status code indicating reason for failure
    """
    try:
        drink = Drink.query.filter_by(id=id).one_or_none()
        if drink:
            drink.delete()
            return jsonify({
                'success': True,
                'delete': id,
            })
        else:
            abort(404)
    except:
        abort(500)


# Error Handling
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
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'internal server error',
    }), 500


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    """
    handles a AuthError exception
    """
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response
