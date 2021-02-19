from flask import jsonify, request
from . import api
from capstone.models import Vehicle


@api.route("/vehicles", methods=["GET"])
def get_vehicles():
    """
    public endpoint GET /vehicles
    contains the vehicle json data representation
    Returns:
        status code 200 and json {"success": True, "vehicles": vehicles} where vehicles is the list of vehicles
        appropriate status code indicating reason for failure
    """
    try:
        vehicles = [v.to_json() for v in Vehicle.query.all()]
        return jsonify({
            "success": True,
            "vehicles": vehicles,
        })
    except:
        abort(500)


@api.route("/vehicles/<int:id>", methods=["GET"])
def get_vehicle(id):
    """
    endpoint GET /vehicles/<id>, where <id> is the existing model id
    responds with a 404 error if <id> is not found
    contains the vehicle json data representation
    Returns:
        status code 200 and json {"success": True, "vehicles": vehicle} where vehicle is a list of single vehicle
        appropriate status code indicating reason for failure
    """
    try:
        vehicle = Vehicle.query.get_or_404(id)
        return jsonify({
            "success": True,
            "vehicles": [vehicle.to_json()],
        })
    except:
        abort(500)


@api.route("/vehicles", methods=["POST"])
# @requires_auth('post:vehicles')
def post_vehicle():
    """
    endpoint POST /vehicles
    creates a new row in the vehicles table
    requires the 'post:vehicles' permission
    contains the vehicle json data representation
    Returns:
        status code 200 and json {"success": True, "vehicles": vehicle} where vehicle an array containing only the newly created vehicle
        appropriate status code indicating reason for failure
    """
    body = request.get_json()

    vehicle = Vehicle(
        VIN=body.get('VIN'),
        make=body.get('make'),
        model=body.get('model'),
        model_year=body.get('model_year'),
        fuel_type=body.get('fuel_type'),
        standard_seat_number=body.get('standard_seat_number'),
        automatic=body.get('automatic'),
    )
    try:
        vehicle.insert()
        return jsonify({
            'success': True,
            'vehicle': [vehicle.to_json()],
        })
    except:
        abort(422)


@app.route('/vehicles/<int:id>', methods=['PATCH'])
# @requires_auth('patch:vehicles')
def patch_vehicle(payload, id):
    """
    endpoint PATCH /vehicles/<id>, where <id> is the existing model id
    responds with a 404 error if <id> is not found
    updates the corresponding row for <id>
    requires the 'patch:vehicles' permission
    contains the vehicle json data representation
    Returns:
        status code 200 and json {"success": True, "vehicles": vehicle} where vehicle an array containing only the updated vehicle
        appropriate status code indicating reason for failure
    """
    try:
        body = request.get_json()
        vehicle = Vehicle.query.get_or_404(id)
        if 'VIN' in body:
            vehicle.VIN = body.get('VIN')
        if 'make' in body:
            vehicle.make = json.dumps(body.get('make'))
        if 'model' in body:
            vehicle.model = body.get('model')
        if 'model_year' in body:
            vehicle.model_year = body.get('model_year')
        if 'fuel_type' in body:
            vehicle.fuel_type = json.dumps(body.get('fuel_type'))
        if 'standard_seat_number' in body:
            vehicle.standard_seat_number = body.get('standard_seat_number')
        if 'automatic' in body:
            vehicle.automatic = body.get('automatic')
        vehicle.update()
        return jsonify({
            'success': True,
            'vehicles': [vehicle.to_json()],
        })
    except:
        abort(500)


@app.route('/vehicles/<int:id>', methods=['DELETE'])
# @requires_auth('delete:vehicles')
def delete_vehicle(payload, id):
    """
    endpoint DELETE /vehicles/<id>, where <id> is the existing model id
    responds with a 404 error if <id> is not found
    deletes the corresponding row for <id>
    requires the 'delete:vehicles' permission
    Returns:
        status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        appropriate status code indicating reason for failure
    """
    try:
        vehicle = Vehicle.query.get_or_404(id)
        vehicle.delete()
        return jsonify({
            'success': True,
            'delete': id,
        })
    except:
        abort(500)
