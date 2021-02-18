import os
from flask import Flask
from models import setup_db


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.route('/')
    def index():
        return "Welcome to the Capstone Car Booking Platform!"

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
