from flask import jsonify, request
from . import api
from capstone.models import Booking

@api.route('/bookings')
def get_bookings():
    # TODO implement to_json()
    try:
        bookings = Booking.query.all()
        return jsonify(booking.to_json())
    except:
        abort(500)

@api.route('/bookings/<int:id>')
def get_booking(id):
    # TODO implement to_json()
    booking = Booking.query.get_or_404(id)
    return jsonify(booking.to_json())