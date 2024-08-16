#!/usr/bin/python3
"""Index"""
from models import storage
from flask import Flask, jsonify
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    """Returns JSON status"""
    return jsonify({"status": "OK"})


@app_views.route('/status', strict_slashes=False)
def count():
    """Retrieves the number of each objects by type
    """
    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")})
