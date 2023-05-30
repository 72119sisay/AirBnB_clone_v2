#!/usr/bin/python3
"""A script that starts a flask web application
Your web application must be listening on 127.0.0.1, port 5000
"""

from flask import Flask

app = Flask("__name__")


@app.route('/', strict_slashes=False)
def hello():
    """Return a given string"""
    return ("Hello HBNB!")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=None)
