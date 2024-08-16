#!/usr/bin/python3
"""Handles all RESTful API actions for States"""
from models.state import State
from flask import jsonify, abort, request
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
    if not request.get_json():
        make_response(jsonify({"error": "Not a JSON"}), 400)

    data = request.get_json()

    if 'name' not in data:
        make_response(jsonify({"error": "Missing name"}), 400)

    new_state = State(**data)
    new_state.save()

    return jsonify(new_state.to_dict()), 201
