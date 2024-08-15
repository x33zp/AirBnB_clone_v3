#!/usr/bin/python3
"""Index"""
from api.v1.views import app_views
from flask import Flask, jsonify


@app.views.route('/status', strict_slashes=False)
def status():
    """Returns a JSON status"""
    return jsonify({"status": "OK"}


@app.views.route('/stats', strict_slashes=False)
def count():
    """Retrieves the number of each object by type
    """
    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("city"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")})
