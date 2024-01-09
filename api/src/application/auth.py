from functools import wraps
from http import HTTPStatus

from flask import current_app, request

from src.application.response import abort_json


def check_api_key(api_key: str):
    vault = current_app.config["VAULT"]

    return vault.check_key(api_key)


def require_api_key(f):
    """Decorator for requiring API keys on the endpoint"""

    @wraps(f)
    def wrapped(*args, **kwargs):
        api_key = request.headers.get("RELAY-API-KEY", None)

        if not api_key:
            return abort_json(HTTPStatus.FORBIDDEN, {"error": "Missing API KEY"})

        if not check_api_key(api_key):
            abort_json(HTTPStatus.FORBIDDEN, {"error": "Invalid API KEY"})

        return f(*args, **kwargs)

    return wrapped
