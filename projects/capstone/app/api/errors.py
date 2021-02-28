from flask import jsonify, request, abort
from . import api

# Error Handling
@api.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'bad request',
    }), 400


@api.errorhandler(401)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'error': 401,
        'message': 'method not allowed',
    }), 401


@api.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'resource not found',
    }), 404


@api.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@api.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'internal server error',
    }), 500
