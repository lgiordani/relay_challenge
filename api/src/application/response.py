from flask import abort, jsonify


def abort_json(status_code: int, data: dict):
    response = jsonify(data)
    response.status_code = status_code

    abort(response)
