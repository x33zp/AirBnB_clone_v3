#!/usr/bin/python3
"""Handles all RESTful API actions for States"""
from models.city import City
from models.state import State
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    city_objs = []
    for city in state.cities:
        city_objs.append(city.to_dict())
    return jsonify(city_objs)


@app_views.route('/cities/<city_id>', methods=['Get'], strict_slashes=False)
def city(city_id):
    """Retrives City by id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a State obj by id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a state object"""
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()

    if 'name' not in data:
        abort(400, description="Missing name")

    new_city = City(**data)
    new_city.state_id = state_id
    new_city.save()

    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a State objectt by id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")

    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
