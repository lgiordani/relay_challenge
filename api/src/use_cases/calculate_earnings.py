from typing import List, Optional, Union

from dateutil.parser import ParserError, isoparse

from src.entities.types import ActivityLogType
from src.rate_cards.rate_cards_calculator import RateCardsCalculator
from src.requests.request import InvalidRequest, Request, ValidRequest
from src.responses.response import ResponseFailure, ResponseSuccess
from src.use_cases import error_codes


def build_calculate_earnings_request(
    tier: Optional[str] = None,
    activity_log: Optional[List[ActivityLogType]] = None,
) -> Request:
    parameters = {"tier": tier, "activity_log": activity_log}

    if tier is None:
        return InvalidRequest(
            parameter="tier",
            error_code=error_codes.MISSING_PARAMETERS,
            message="Missing",
            request_parameters=parameters,
        )

    if activity_log is None:
        return InvalidRequest(
            parameter="activity_log",
            error_code=error_codes.MISSING_PARAMETERS,
            message="Missing",
            request_parameters=parameters,
        )

    if tier not in RateCardsCalculator.tiers.keys():
        return InvalidRequest(
            parameter="tier",
            error_code=error_codes.INVALID_TIER,
            message=f"Invalid tier code: {tier}",
            request_parameters=parameters,
        )

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


def calculate_earnings_use_case(
    request: Request,
) -> Union[ResponseSuccess, ResponseFailure]:
    tier = request.parameters["tier"]
    activity_log = request.parameters["activity_log"]

    try:
        rcc = RateCardsCalculator(tier)
        earnings = rcc.process(activity_log)

        return ResponseSuccess(earnings.asdict())
    except Exception as exc:  # pylint: disable=broad-exception-caught
        return ResponseFailure(error_codes.UNKNOWN_ERROR, exc)
