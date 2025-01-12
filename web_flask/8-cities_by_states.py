#!/usr/bin/python3
"""
A Script that imports flask, render_template, storage
and state and displays it after it's sorted in order
"""
from flask import Flask, render_template
from models import storage
from models.city import City
from models.state import State

app = Flask(__name__)


@app.route("/cities_by_states", strict_slashes=False)
def states_list():
    """Displays an HTML page with a list of all State objects in DBStorage
    States are sorted by name
    """
    states = storage.all(State)
    return render_template("8-cities_by_states.html", states=states)


@app.teardown_appcontext
def teardown(exc):
    """Remove the current SQLAlchemy session."""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
