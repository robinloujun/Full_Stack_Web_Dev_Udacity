Capstone Car Booking Platform
-----

## Introduction

This platform is a car booking site that facilitates the discovery and bookings as clients. This site lets the clients list all available vehicles, check the information, and decide booking a vehicle for his own purpose.

## Getting Started

### 1. Install Dependencies
Our tech stack will include the following:
 * **virtualenv** as a tool to create isolated Python environments
 * **SQLAlchemy ORM** to be our ORM library of choice
 * **PostgreSQL** as our database of choice
 * **Python3** and **Flask** as our server language and server framework
 * **Flask-Migrate** for creating and running schema migrations

It is recommended to use a virtual environment while developing and building:

```
python3 -m venv venv
source venv/bin/activate
```

Then you can download and install the dependencies mentioned above using `pip` as:
```
pip install -r requirements.txt
```

### 2. Run the development server:
```
export FLASK_APP=capstone
export FLASK_CONFIG=development
flask run
```

### 3. API Documents

The Capstone API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.

### Endpoints for Vehicle

* GET '/vehicles'
* GET '/vehicles/int:vin'
* POST '/vehicles'
* PATCH '/vehicles/int:vin'
* DELETE '/vehicles/int:vin'

GET '/vehicles'

* Fetches a dictionary of vehicles in which the keys are the vins (vehicle identification number) and the value is the corresponding json content of the vehicles
* Request Arguments: None
* Returns: 
    * An object with a single key, categories, that contains a object of id: category_string key:value pairs.

```
{
    "vehicles": [
        {
            "vin": 11234,
            "make": "Mercedes-Benz",
            "model": "A Class Sedan",
            "model_year": 2015,
            "fuel_type": "petrol",
            "standard_seat_number": 5,
            "automatic": true,
            "bookings_count": 0,
        },
        {
            "vin": 10006,
            "make": "BMW",
            "model": "530 Sedan",
            "model_year": 2010,
            "fuel_type": "petrol",
            "standard_seat_number": 5,
            "automatic": true,
            "bookings_count": 0,
        },
    ],
    "success": true
}
```

GET '/vehicles/int:vin'

* Fetches a dictionary of vehicle, which has the given vin.
* Request Arguments: None
* Returns:
    * vehicle: a list of dictionary of vehicle in pre-defined format

```
{
    "vehicle": [
        {
            "vin": 11234,
            "make": "Mercedes-Benz",
            "model": "A Class Sedan",
            "model_year": 2015,
            "fuel_type": "petrol",
            "standard_seat_number": 5,
            "automatic": true,
            "bookings_count": 0,
        }
    ],
    "success": true
}
```

POST '/vehicles'

* Creates a vehicle.
* Request Arguments: dictionary of the vehicle information to update
* Returns:
    * vehicle_vin: vin of the updated vehicle

```
{
    "success": true,
    "vehicle_vin": 1225,
}
```

PATCH '/vehicles/int:vin'

* Updates a vehicle with given vin.
* Request Arguments: dictionary of the vehicle information to update
* Returns:
    * vehicle_vin: vin of the posted vehicle

```
{
    "success": true,
    "vehicle_vin": 1225,
}
```

DELETE '/vehicles/int:vin'

* Deletes a vehicle with given vin.
* Request Arguments: None
* Returns:
    * vehicle_vin: vin of the deleted vehicle

```
{
    "success": true,
    "vehicle_vin": 1225,
}
```

# Endpoints for Client

* GET '/clients'
* GET '/clients/int:id'
* POST '/clients'
* PATCH '/clients/int:id'
* DELETE '/clients/int:id'

### Endpoints for Booking

* GET '/bookings'
* GET '/bookings/int:id'
* POST '/bookings'
* PATCH '/bookings/int:id'
* DELETE '/bookings/int:id'


4. **Testing**

To run the tests, run

```
dropdb capstone_test
createdb capstone_test
python test_capstone.py
```

5. **Verify on the Browser**<br>
Navigate to project homepage [http://127.0.0.1:5000/](http://127.0.0.1:5000/) or [http://localhost:5000](http://localhost:5000) 


## Author

Jun Lou

