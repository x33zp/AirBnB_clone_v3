#!/usr/bin/python3
"""Index"""
from api.v1.views import app_views
from flask import Flask, jsonify


@app.views.route('/status', strict_slashes=False)
def status():
    """Returns a JSON status"""
    return jsonify({"status": "OK"})
