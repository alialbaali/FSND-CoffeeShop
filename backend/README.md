# Coffee Shop Backend

## Getting Started

### Dependencies

Dependencies are listed in the `requirements.txt` file. 
Run `pip3 install -r requirements.txt` to install them.

### Tech Stack

* SQLAlchemy ORM
* PostgreSQL
* Python3 and Flask
* Flask-Migrate
* Flask-CORS
* HTML, CSS, and Javascript


## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Roles 
- Barista
    - can `get:drinks-detail`
- Manager
    - can perform all actions


## Endpoints
### Categories

#### `GET /drinks`

##### `Permissons: None`

- Fetches all the drinks from the database
- Request Arguments : None
- Returns: a list of drinks `Short-Format`

#### `Response`
```json
{ 
    "success": true,
    "drinks": [
        {
            "id" : 1, 
            "title" : "Mocha",
            "recipe" : {
              "color": "Brownish",
              "parts": "Chocolate, Coffee"
            }
        },
        {
            "id" : 2, 
            "title" : "Cappuccino",
            "recipe" : {
              "color": "Yellowish",
              "parts": "Milk, Espresso"
            }
        }
    ]
}
```

#### `GET /drinks-detail`

##### `Permissons: get:drinks-detail`

- Fetches all the drinks from the database
- Request Arguments : Token payload
- Returns: a list of drinks `Long-Format`

#### `Response`
```json
{ 
    "success": true,
    "drinks": [
        {
            "id" : 1, 
            "title" : "Mocha",
            "recipe" : "chocolate-flavoured variant of a cafe latte"
        },
        {
            "id" : 2, 
            "title" : "Cappuccino",
            "recipe" : "an espresso-based coffee drink that originated in Italy, and is traditionally prepared with steamed milk foam"
        }
    ]
}
```

#### `POST /drinks`

##### `Permissons: post:drinks`

- Inserts a drink to the db using the information provided
- Request Arguments : Token payload
- Returns: the inserted drink `Long-Format`

#### `Response`
```json
{ 
    "success": true,
    "drinks": [
        {
            "id" : 2, 
            "title" : "Cappuccino",
            "recipe" : "an espresso-based coffee drink that originated in Italy, and is traditionally prepared with steamed milk foam"
        }
    ]
}
```

#### `PATCH /drinks/<int:drink_id>`

##### `Permissons: patch:drinks`

- Updates drink information and commit the changes to the db
- Request Arguments : Token payload and drink id
- Returns: the updated drink `Long-Format`

#### `Response`
```json
{ 
    "success": true,
    "drinks": [
        {
            "id" : 2, 
            "title" : "Cappuccino",
            "recipe" : "an espresso-based coffee drink that originated in Italy, and is traditionally prepared with steamed milk foam"
        }
    ]
}
```

#### `DELETE /drinks/<int:drink_id>`

##### `Permissons: delete:drinks`

- Updates drink information and commit the changes to the db
- Request Arguments : Token payload and drink id
- Returns: the updated drink `Long-Format`

#### `Response`
```json
{ 
    "success": true,
    "drinks": [
        {
            "id" : 2, 
            "title" : "Cappuccino",
            "recipe" : "an espresso-based coffee drink that originated in Italy, and is traditionally prepared with steamed milk foam"
        }
    ]
}
```

## Status Codes
- `200` : Request has been fulfilled
- `201` : Entity has been created
- `401` : Unauthorized
- `404` : Resource not found
- `422` : Wrong info provided