#!/usr/bin/python3
"""Flask App"""
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.teardown_appcontext
def teardown_db(exception):
    """This method is called after each request to close the storage"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """Returns a JSON-formatted 404 status code response"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    import os
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
