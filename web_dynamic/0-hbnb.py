#!/usr/bin/python3
""" A script that starts a Flask web application """

from flask import Flask, render_template
from models import storage
from uuid import uuid4

app = Flask(__name__)


@app.route('/0-hbnb/', strict_slashes=False)
def hbnb():
    """ Displays a HTML page """
    state = storage.all("State")
    amenity = storage.all("Amenity")
    place = storage.all("Place")
    return render_template('0-hbnb.html', states=state,
            amenities=amenity, places=place, cache_id=uuid4())


@app.teardown_appcontext
def teardown(exc):
    """ Removes current SQLAlchemy session """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
