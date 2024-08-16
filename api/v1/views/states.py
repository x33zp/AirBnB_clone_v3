#!/usr/bin/python3
"""Handles all RESTful API actions for States"""
from models.state import State
from flask import jsonify, abort
from api.v1.views import app_views
from models import storage

#@app_views.route('/status', strict_slashes=False)
"""
def get_states():
    Retrives the list of all state objs
    all_state = storage.all(State).values()
    list_states = []
    for state in all_states:
        list_states.append(state.to_dict())

    return jsonify(list_states)
"""
@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id=None):
    if state_id == None:
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
