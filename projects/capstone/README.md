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

* Fetches a dictionary of vehicles with json content of the vehicles
* Request Arguments: None
* Returns: 
    * A JSON format with list of vehicles objects

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
    * vehicles: a list of dictionary of vehicle in pre-defined format

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
        }
    ],
    "success": true
}
```

POST '/vehicles'

* Creates a vehicle.
* Request Arguments: dictionary of the vehicle information to post
* Returns:
    * vehicle_vin: vin of the posted vehicle

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
    * vehicle_vin: vin of the updated vehicle

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

GET '/clients'

* Fetches a dictionary of clients with json content of the clients
* Request Arguments: None
* Returns: 
    * A JSON format with list of clients objects

```
{
    "clients": [
        {
            "id": 1912,
            "forename": "Alan",
            "surname": "Turing",
            "email": "alan.turing@mustermann.com",
        },
        {
            "id": 1903,
            "forename": "Alonzo",
            "surname": "Church",
            "email": "alonzo.church@mustermann.com",
        },
        {
            "id": 1880,
            "forename": "Oswald",
            "surname": "Veblen",
            "email": "oswald.veblen@mustermann.com",
        },
    ],
    "success": true
}
```

GET '/clients/int:id'

* Fetches a dictionary of client, which has the given id.
* Request Arguments: None
* Returns:
    * clients: a list of dictionary of client in pre-defined format

```
{
    "clients": [
        {
            "forename": "Alan",
            "surname": "Turing",
            "email": "alan.turing@mustermann.com",
        }
    ],
    "success": true
}
```

POST '/clients'

* Creates a client.
* Request Arguments: dictionary of the client information to post
* Returns:
    * client_id: id of the posted client

```
{
    "success": true,
    "client_id": 101,
}
```

PATCH '/clients/int:id'

* Updates a client with given id.
* Request Arguments: dictionary of the client information to update
* Returns:
    * client_id: id of the updated client

```
{
    "success": true,
    "client_id": 101,
}
```

DELETE '/clients/int:id'

* Deletes a client with given id.
* Request Arguments: None
* Returns:
    * client_id: id of the deleted client

```
{
    "success": true,
    "client_id": 101,
}
```


### Endpoints for Booking

* GET '/bookings'
* GET '/bookings/int:id'
* POST '/bookings'
* PATCH '/bookings/int:id'
* DELETE '/bookings/int:id'

GET '/bookings'

* Fetches a dictionary of bookings with json content of the bookings
* Request Arguments: None
* Returns: 
    * A JSON format with list of bookings objects

```
{
    "bookings": [
        {
            "booking_id": 886,
            "vehicle_VIN": "11234",
            "client_id": "1912",
            "start_datetime": "2018-08-08T09:00:00.000000",
            "end_datetime": "2018-08-10T21:00:00.000000",
        },
        {
            "booking_id": 1886,
            "vehicle_VIN": "10006",
            "client_id": "1880",
            "start_datetime": "2021-02-14T09:00:00.000000",
            "end_datetime": "2021-02-14T20:00:00.000000",
        },
    ],
    "success": true
}
```

GET '/bookings/int:id'

* Fetches a dictionary of booking, which has the given id.
* Request Arguments: None
* Returns:
    * bookings: a list of dictionary of booking in pre-defined format

```
{
    "bookings": [
        {
            "booking_id": 886,
            "vehicle_VIN": "11234",
            "client_id": "1912",
            "start_datetime": "2018-08-08T09:00:00.000000",
            "end_datetime": "2018-08-10T21:00:00.000000",
        }
    ],
    "success": true
}
```

POST '/bookings'

* Creates a booking.
* Request Arguments: dictionary of the booking information to post
* Returns:
    * booking_id: id of the posted booking

```
{
    "success": true,
    "booking_id": 886,
}
```

PATCH '/bookings/int:id'

* Updates a booking with given id.
* Request Arguments: dictionary of the booking information to update
* Returns:
    * booking_id: id of the updated booking

```
{
    "success": true,
    "booking_id": 886,
}
```

DELETE '/bookings/int:id'

* Deletes a booking with given id.
* Request Arguments: None
* Returns:
    * booking_id: id of the deleted booking

```
{
    "success": true,
    "booking_id": 886,
}
```

### 4. Testing

To run the tests, run

```
dropdb capstone_test
createdb capstone_test
python test_capstone.py
```
### 5. Verify on the Browser:
Navigate to project homepage [http://127.0.0.1:5000/](http://127.0.0.1:5000/) or [http://localhost:5000](http://localhost:5000) 


## Author

Jun Lou

