#!/usr/bin/python3
"""
A script that starts flask, listens on host 0.0.0.0, on port 5000
"""

from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """returns Hello HBNB string"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def print_hbnb():
    """returns string HBNB"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_text(text):
    """prints C followed by value"""
    text_spaces = text.replace("_", " ")
    return f"C {text_spaces}"


@app.route("/python/<text>", strict_slashes=False)
@app.route("/python", strict_slashes=False)
def print_python_text(text="is cool"):
    """Print python followed by arguments"""
    text_spaces = text.replace("_", " ")
    return f"Python {text_spaces}"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
