import os
from re import T
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import requires_auth
from .errors import *

app = Flask(__name__)
setup_db(app)
CORS(app)


db_drop_and_create_all()

# ROUTES

@app.route('/drinks',methods = ['GET'])
def drinks():
    drinks = Drink.query.all()
    
    if(len(drinks) < 1):
        raise not_found()
    
    return jsonify({
        'success' : True,
        'drinks': [drink.short() for drink in drinks]
    })


@app.route('/drinks-detail', methods = ['GET'])
@requires_auth('get:drinks-details')
def drink_details(payload):
    drinks = Drink.query.all()

    if(len(drinks) < 1):
        raise not_found()
    
    return jsonify({
        'success':True,
        'drinks': [drink.long() for drink in drinks]
    })


@app.route('/drinks', methods = ['POST'])
@requires_auth('post:drinks')
def make_drink(payload):
 body = request.get_json()

 for required in ['title', 'recipe']:
    if required not in body or body[required]=='':
        raise unprocessable({
            'status' : "request_invalid",
            'message' : "Title and recipe is needed"
        })
    
    try:
        drink = Drink(title = body['title'],
                recipe = json.dumps(body['recipe']))
        drink.insert()

        drinks = Drink.query.all()
        if(len(drinks) < 1): 
            raise not_found(404)
        
        return jsonify({
            'success':True,
            'drinks': [drink.long() for drink in drinks]
        })

    except:
        raise database_error()


@app.route('/drinks/<int:drink_id>', methods = ['PATCH'])
@requires_auth('patch:drinks')
def edit_drink(payload, drink_id):
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    if not drink:
        raise not_found()
    
    body = request.get_json()
    for required in ['title', 'recipe']:
        if required not in body or body[required] == '':
             raise unprocessable({
                'status' : "request_invalid",
                'message' : f"{required} is required, string cannot be empty"
        })

    try:

        title  = body.get('title', drink.title)
        recipe = body.get('recipe')

        drink.title = title
        drink.recipe = json.dumps(recipe) if recipe else drink.recipe
        drink.update()


        drinks = Drink.query.all()
        if(len(drinks) < 1):
            raise not_found()
        
        return jsonify({
            'success': True,
            'drinks': [drink.long() for drink in drinks]
        }) 
    
    except:
        raise database_error()


@app.route('/drinks/<int:drink_id>' , methods=['DELETE'])
@requires_auth('delete:drinks')
def remove_drink(payload, drink_id):
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    if not drink:
        raise not_found()

    try:
        drink.delete()
        return jsonify({

            'sucess': True,
            'deleted': drink_id
        })

    except:
        raise database_error()

# Error Handling


@app.errorhandler(500)
def error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'Something is probably wrong here'
    }), 500

@app.errorhandler(api_error)
def error(error):
    return jsonify({
        'sucess': False,
        'status': error.error['status'],
        'error': error.code,
        'message': error.error['message']
    }),error.code


@app.errorhandler(auth_error)
def error(error):
       return jsonify({
        'sucess': False,
        'status': error.error['status'],
        'error': error.code,
        'message': error.error['message']
    
    }),error.code

