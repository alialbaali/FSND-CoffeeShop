from flask import Flask, request, jsonify, abort
from flask_cors import CORS

from .auth.auth import AuthError, requires_auth
from .database.models import db_drop_and_create_all, setup_db, Drink

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the database
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()


# CORS Headers
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# ROUTES
"""
Route GET '/drinks'

:param None

:permission None (publicly available)

Queries all the drinks from db

:returns 'short' formatted drinks (JSON)

"""


@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()

    formatted_drinks = [drink.short() for drink in drinks]

    return jsonify({
        'success': True,
        'drinks': formatted_drinks
    })


"""
Route GET '/drinks-detail'

:param payload (str) 'token payload'

:permission 'get:drinks-detail' (available to Manager and (Barista)

Queries all drinks from db

:raises 404 Not Found

:returns 'long' formatted drinks (JSON)

"""


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    drinks = Drink.query.all()

    # if not drinks:
    #     abort(404)

    formatted_drinks = [drink.long() for drink in drinks]

    return jsonify({
        'success': True,
        'drinks': formatted_drinks
    })


"""
Route POST '/drinks'

:param payload (str) 'token payload'

:permission 'post:drinks' (available to Manager)

Retrieves drink information from request's body (JSON)

Inserts a drink to the db using the information provided

:raises 422 Unprocessable

:returns a list with 'long' formatted inserted drink  (JSON)

"""


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload):
    body = request.get_json()

    try:

        title = body['title']
        recipe = body['recipe']

        drink = Drink(title=title, recipe=recipe)
        drink.insert()

        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })

    except Exception:
        abort(422)


"""
Route PATCH '/drinks/1'

:param drink_id (int)
:param payload (str) 'token payload'

:permission 'patch:drinks' (available to Manager)

Retrieves drink information from request's body (JSON)

Queries db using the provided id parameter 

Updates drink information and commit the changes to the db

:raises 404 Not Found
:raises 422 Unprocessable

:returns a list with 'long' formatted updated drink  (JSON)

"""


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(drink_id, payload):
    body = request.get_json()

    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

    if not drink:
        abort(404)

    try:

        drink.title = body['title']
        drink.recipe = body['recipe']

        drink.update()

        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })

    except Exception:
        abort(422)


"""
Route DELETE '/drinks/1'

:param drink_id (int)
:param payload (str) 'token payload'

:permission 'delete:drinks' (available to Manager)

Retrieves drink information from request's body (JSON)

Queries db using the provided id parameter 

Updates drink information and commit the changes to the db

:raises 404 Not Found
:raises 422 Unprocessable

:returns the deleted drink id

"""


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(drink_id, payload):
    drink = Drink.query.filter(Drink.id == drink_id)

    if not drink:
        abort(404)

    try:

        drink.delete()

        return jsonify({
            'success': True,
            'delete': drink.id
        })

    except Exception:
        abort(422)


"""
Error Handling
"""


# Error Handler (422) Unprocessable
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


# Error Handler (404) Not Found
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

# Error Handler (401) Unauthorized
@app.errorhandler(AuthError)
def not_authenticated(auth_error):
    return jsonify({
        "success": False,
        "error": auth_error.status_code,
        "message": auth_error.error
    }), 401
