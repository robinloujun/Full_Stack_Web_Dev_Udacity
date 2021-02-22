from flask import jsonify, request
from . import api
from ..auth.auth import requires_auth
from ..models import Booking


@api.route("/bookings", methods=["GET"])
def get_bookings():
    """
    public endpoint GET /bookings
    contains the booking json data representation
    Returns:
        status code 200 and json {"success": True, "bookings": bookings} where bookings is the list of bookings
        appropriate status code indicating reason for failure
    """
    try:
        bookings = [b.to_json() for b in Booking.query.all()]
        return jsonify({
            "success": True,
            "bookings": bookings,
        })
    except:
        abort(500)


@api.route("/bookings/<int:id>", methods=["GET"])
def get_booking(id):
    """
    endpoint GET /bookings/<id>, where <id> is the existing model id
    responds with a 404 error if <id> is not found
    contains the booking json data representation
    Returns:
        status code 200 and json {"success": True, "bookings": booking} where booking is a list of single booking
        appropriate status code indicating reason for failure
    """
    try:
        booking = Booking.query.get_or_404(id)
        return jsonify({
            "success": True,
            "bookings": [booking.to_json()],
        })
    except:
        abort(500)


@api.route("/bookings", methods=["POST"])
@requires_auth('post:bookings')
def post_booking():
    """
    endpoint POST /bookings
    creates a new row in the bookings table
    requires the 'post:bookings' permission
    contains the booking json data representation
    Returns:
        status code 200 and json {"success": True, "bookings": booking} where booking an array containing only the newly created booking
        appropriate status code indicating reason for failure
    """
    body = request.get_json()

    booking = Booking(
        vehicle_VIN=body.get('vehicle_VIN'),
        client_id=body.get('client_id'),
        start_datetime=body.get('start_datetime'),
        end_datetime=body.get('end_datetime'),
    )
    try:
        booking.insert()
        return jsonify({
            'success': True,
            'booking': [booking.to_json()],
        })
    except:
        abort(422)


@api.route('/bookings/<int:id>', methods=['PATCH'])
@requires_auth('patch:bookings')
def patch_booking(payload, id):
    """
    endpoint PATCH /bookings/<id>, where <id> is the existing model id
    responds with a 404 error if <id> is not found
    updates the corresponding row for <id>
    requires the 'patch:bookings' permission
    contains the booking json data representation
    Returns:
        status code 200 and json {"success": True, "bookings": booking} where booking an array containing only the updated booking
        appropriate status code indicating reason for failure
    """
    try:
        body = request.get_json()
        booking = Booking.query.get_or_404(id)
        if 'vehicle_VIN' in body:
            booking.vehicle_VIN = body.get('vehicle_VIN')
        if 'client_id' in body:
            booking.client_id = json.dumps(body.get('client_id'))
        if 'start_datetime' in body:
            booking.start_datetime = body.get('start_datetime')
        if 'end_datetime' in body:
            booking.end_datetime = json.dumps(body.get('end_datetime'))
        booking.update()
        return jsonify({
            'success': True,
            'bookings': [booking.to_json()],
        })
    except:
        abort(500)


@api.route('/bookings/<int:id>', methods=['DELETE'])
@requires_auth('delete:bookings')
def delete_booking(payload, id):
    """
    endpoint DELETE /bookings/<id>, where <id> is the existing model id
    responds with a 404 error if <id> is not found
    deletes the corresponding row for <id>
    requires the 'delete:bookings' permission
    Returns:
        status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        appropriate status code indicating reason for failure
    """
    try:
        booking = Booking.query.get_or_404(id)
        booking.delete()
        return jsonify({
            'success': True,
            'delete': id,
        })
    except:
        abort(500)
