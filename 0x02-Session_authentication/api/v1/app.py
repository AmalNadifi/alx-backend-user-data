#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
# Load the appropriate authentication instance
# based on the environment variable AUTH_TYPE
auth_type = os.getenv("AUTH_TYPE")
if auth_type:
    if auth_type == "auth":
        from api.v1.auth.auth import Auth
        auth = Auth()
    elif auth_type == "basic_auth":
        from api.v1.auth.basic_auth import BasicAuth
        auth = BasicAuth()
    else:
        raise ValueError(
                "Invalid value. Supported values: 'auth', 'basic_auth'"
                )


@app.before_request
def before_request():
    """Handler for before request filtering"""
    if auth is None:
        return  # Do nothing if auth is not set

    excluded_paths = [
            '/api/v1/status/',
            '/api/v1/unauthorized/',
            '/api/v1/forbidden/'
            ]
    if (request.path not in excluded_paths and
            auth.require_auth(request.path, excluded_paths)):
        # Check if authentication is required for the request path
        if auth.authorization_header(request) is None:
            abort(401)  # Authorization header missing, raise 401 error
        if auth.current_user(request) is None:
            abort(403)  # Current user not authenticated, raise 403 error


# Error handling
@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
