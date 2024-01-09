import os

import requests

api_host = os.environ.get("RELAY_API_HOST", "localhost")
api_port = os.environ.get("RELAY_API_PORT")
api_key = os.environ.get("RELAY_API_KEY")

BASE_URL = f"http://{api_host}:{api_port}"
DEFAULT_HEADERS = {"RELAY-API-KEY": api_key}


def request(method, relative_url="", json=None, params=None):
    func = getattr(requests, method.lower())
    full_url = f"{BASE_URL}{relative_url}"
    headers = DEFAULT_HEADERS
    json = json or {}
    params = params or {}

    response = func(full_url, headers=headers, json=json, params=params)

    return {"status_code": response.status_code, "json": response.json()}
