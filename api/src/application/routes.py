from http import HTTPStatus

from flask import Blueprint, current_app, jsonify, request

from src.application.auth import require_api_key

from src.application.response import abort_json
from src.use_cases import error_codes

from src.use_cases.calculate_earnings import (
    build_calculate_earnings_request,
    calculate_earnings_use_case,
)

route_blueprint = Blueprint("route_blueprint", __name__)


@route_blueprint.route("/", methods=["GET"])
def root():
    return jsonify({"status": "OK"})


@route_blueprint.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "OK"})


@route_blueprint.route("/earnings/<tier>", methods=["POST"])
@require_api_key
def calculate_earnings(tier):
    request_data = request.get_json()

    # WEB REQUEST TO USE CASE REQUEST
    use_case_request = build_calculate_earnings_request(tier, request_data)
    response = calculate_earnings_use_case(use_case_request)

    # USE CASE RESPONSE TO WEB RESPONSE
    if not response:
        data = {
            "message": response.value["message"],
            "code": response.value["error_code"],
        }

        response_codes = {
            error_codes.INVALID_TIER: HTTPStatus.BAD_REQUEST,
            error_codes.MISSING_PARAMETERS: HTTPStatus.BAD_REQUEST,
            error_codes.INVALID_ACTIVITY: HTTPStatus.BAD_REQUEST,
        }

        status_code = response_codes.get(
            response.value["error_code"], HTTPStatus.INTERNAL_SERVER_ERROR
        )

        abort_json(status_code, data)

    return jsonify(response.value), HTTPStatus.CREATED
