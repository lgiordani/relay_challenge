from datetime import datetime
from dateutil.parser import isoparse, ParserError

from typing import List
from src.entities.types import ActivityLogType

from src.requests.request import InvalidRequest, Request, ValidRequest
from src.responses.response import (
    ResponseFailure,
    ResponseSuccess,
    build_response_from_invalid_request,
)

from src.use_cases import error_codes


def build_calculate_earnings_request(
    activity_log: List[ActivityLogType],
) -> Request:
    parameters = {"activity_log": activity_log}

    for activity in activity_log:
        if set(activity.keys()) != set(["route_id", "attempt_date_time", "success"]):
            return InvalidRequest(
                parameter="activity_log",
                error_code=error_codes.INVALID_ACTIVITY,
                message=f"Invalid format for activity: {activity}",
                request_parameters=parameters,
            )

        try:
            isoparse(activity["attempt_date_time"])
        except (ParserError, ValueError):
            return InvalidRequest(
                parameter="activity_log",
                error_code=error_codes.INVALID_ACTIVITY,
                message=f"Invalid format for activity date: {activity}",
                request_parameters=parameters,
            )

    return ValidRequest(parameters)


# def calculate_earnings_use_case(
#     datastore: Datastore, request: Request, email_validator=None
# ) -> Union[ResponseSuccess, ResponseFailure]:
#     if not request:
#         return build_response_from_invalid_request(request)

#     user_id = request.parameters["user_id"]
#     user_id = user_id or generate_uuid()

#     otp_secret = request.parameters["otp_secret"]
#     password = request.parameters["password"]

#     try:
#         email = email_formatter(request.parameters["email"], validator=email_validator)
#     except ValueError as exc:
#         return ResponseFailure(error_codes.INVALID_CREDENTIALS, exc)

#     try:
#         user = datastore.calculate_earnings(
#             user_id,
#             email=email,
#             password=password,
#             otp_secret=otp_secret,
#         )

#         return ResponseSuccess(user.user_id)

#     except UserAlreadyExists as exc:
#         return ResponseFailure(error_codes.USER_ALREADY_EXISTS, exc)
#     except Exception as exc:
#         return ResponseFailure(error_codes.UNKNOWN_ERROR, exc)
