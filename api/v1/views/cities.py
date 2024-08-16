#!/usr/bin/python3
"""Handles all RESTful API actions for States"""
from models.city import City
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage


@app_views.route('/cities', methods=['GET'], strict_slashes=False)
@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id=None):
    if city_id is None:
        all_cities = storage.all(City).values()
        city_objs = []
        for city in all_cities:
            city_objs.append(city.to_dict())
        return jsonify(city_objs)
    else:
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
    return jsonify({})


@app_views.route('/cities', methods=['POST'], strict_slashes=False)
def create_city():
    """Creates a state object"""
    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()

    if 'name' not in data:
        abort(400, description="Missing name")

    new_state = City(**data)
    new_state.save()

    return make_response(jsonify(new_state.to_dict()), 201)

@app_views.route('/citiess/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a State objectt by id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()

    ignore_keys = ['id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    storage.save()

    return make_response(jsonify(city.to_dict()), 200)
