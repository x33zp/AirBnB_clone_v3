#!/usr/bin/python3
"""Handles all RESTful API actions for States"""
from models.state import State
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id=None):
    if state_id is None:
        all_states = storage.all(State).values()
        state_objs = []
        for state in all_states:
            state_objs.append(state.to_dict())
        return jsonify(state_objs)
    else:
        state = storage.get(State, state_id)
        if not state:
            abort(404)
        return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State obj by id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    storage.delete(state)
    storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a state object"""
    if not request.is_json():
        abort(400, description="Not a JSON")

    data = request.get_json()

    if 'name' not in data:
        abort(400, description="Missing name")

    new_state = State(**data)
    new_state.save()

    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State objectt by id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.is_json():
        abort(400, description="Not a JSON")

    data = request.get_json()

    ignore_keys = ['id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    storage.save()

    return make_response(jsonify(state.to_dict()), 200)
