from flask import jsonify, request
from . import api
from capstone.models import Client


@api.route("/clients", methods=["GET"])
def get_clients():
    """
    public endpoint GET /clients
    contains the client json data representation
    Returns:
        status code 200 and json {"success": True, "clients": clients} where clients is the list of clients
        appropriate status code indicating reason for failure
    """
    try:
        clients = [c.to_json() for c in Client.query.all()]
        return jsonify({
            "success": True,
            "clients": clients,
        })
    except:
        abort(500)


@api.route("/clients/<int:id>", methods=["GET"])
def get_client(id):
    """
    endpoint GET /clients/<id>, where <id> is the existing model id
    responds with a 404 error if <id> is not found
    contains the client json data representation
    Returns:
        status code 200 and json {"success": True, "clients": client} where client is a list of single client
        appropriate status code indicating reason for failure
    """
    try:
        client = Client.query.get_or_404(id)
        return jsonify({
            "success": True,
            "clients": [client.to_json()],
        })
    except:
        abort(500)


@api.route("/clients", methods=["POST"])
# @requires_auth('post:clients')
def post_client():
    """
    endpoint POST /clients
    creates a new row in the clients table
    requires the 'post:clients' permission
    contains the client json data representation
    Returns:
        status code 200 and json {"success": True, "clients": client} where client an array containing only the newly created client
        appropriate status code indicating reason for failure
    """
    body = request.get_json()

    client = Client(
        forename=body.get('forename'),
        surname=body.get('surname'),
        email=body.get('email'),
    )
    try:
        client.insert()
        return jsonify({
            'success': True,
            'client': [client.to_json()],
        })
    except:
        abort(422)


@app.route('/clients/<int:id>', methods=['PATCH'])
@requires_auth('patch:clients')
def patch_client(payload, id):
    """
    endpoint PATCH /clients/<id>, where <id> is the existing model id
    responds with a 404 error if <id> is not found
    updates the corresponding row for <id>
    requires the 'patch:clients' permission
    contains the client json data representation
    Returns:
        status code 200 and json {"success": True, "clients": client} where client an array containing only the updated client
        appropriate status code indicating reason for failure
    """
    try:
        body = request.get_json()
        client = Client.query.get_or_404(id)
        if 'forename' in body:
            client.forename = body.get('forename')
        if 'surname' in body:
            client.surname = json.dumps(body.get('surname'))
        if 'email' in body:
            client.email = body.get('email')
        client.update()
        return jsonify({
            'success': True,
            'clients': [client.to_json()],
        })
    except:
        abort(500)


@app.route('/clients/<int:id>', methods=['DELETE'])
@requires_auth('delete:clients')
def delete_client(payload, id):
    """
    endpoint DELETE /clients/<id>, where <id> is the existing model id
    responds with a 404 error if <id> is not found
    deletes the corresponding row for <id>
    requires the 'delete:clients' permission
    Returns:
        status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        appropriate status code indicating reason for failure
    """
    try:
        client = Client.query.get_or_404(id)
        client.delete()
        return jsonify({
            'success': True,
            'delete': id,
        })
    except:
        abort(500)
