#!/usr/bin/python3
"""Handles all RESTful API actions for Amenity"""
from models.user import User
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id=None):
    """Get User"""
    if user_id is None:
        all_users = storage.all(User).values()
        user_objs = []
        for user in all_users:
            user_objs.append(user.to_dict())
        return jsonify(user_objs)
    else:
        user = storage.get(User, user_id)
        if not user:
            abort(404)
        return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a USer obj by id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    storage.delete(user)
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a User object"""
    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()

    if 'name' not in data:
        abort(400, description="Missing name")

    new_user = User(**data)
    new_user.save()

    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """Updates a User objectt by id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()

    ignore_keys = ['id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    storage.save()

    return make_response(jsonify(user.to_dict()), 200)
