from unittest import mock

from src.use_cases import error_codes
from src.use_cases.calculate_earnings import build_calculate_earnings_request


def test_calculate_earnings_request(test_activity_log):
    request = build_calculate_earnings_request("bronze", test_activity_log)

    assert bool(request) is True
    assert request.parameters == {"tier": "bronze", "activity_log": test_activity_log}


def test_calculate_earnings_request_empty_log():
    request = build_calculate_earnings_request("bronze", [])

    assert bool(request) is True
    assert request.parameters == {"tier": "bronze", "activity_log": []}


def test_calculate_earnings_request_missing_tier(test_activity_log):
    request = build_calculate_earnings_request(activity_log=test_activity_log)

    assert bool(request) is False
    assert request.parameters == {"tier": None, "activity_log": test_activity_log}
    assert request.error == {
        "parameter": "tier",
        "message": "Missing",
        "error_code": error_codes.MISSING_PARAMETERS,
    }


@mock.patch("src.use_cases.calculate_earnings.RateCardsCalculator")
def test_calculate_earnings_request_wrong_tier(mock_rcc, test_activity_log):
    mock_rcc.tiers = {}

    request = build_calculate_earnings_request("bronze", test_activity_log)

    assert bool(request) is False
    assert request.parameters == {"tier": "bronze", "activity_log": test_activity_log}
    assert request.error == {
        "parameter": "tier",
        "message": "Invalid tier code: bronze",
        "error_code": error_codes.INVALID_TIER,
    }


def test_calculate_earnings_request_missing_activity_log(test_activity_log):
    request = build_calculate_earnings_request(tier="bronze")

    assert bool(request) is False
    assert request.parameters == {"tier": "bronze", "activity_log": None}
    assert request.error == {
        "parameter": "activity_log",
        "message": "Missing",
        "error_code": error_codes.MISSING_PARAMETERS,
    }


def test_calculate_earnings_request_missing_key_route_id(test_activity_log):
    test_activity_log[0].pop("route_id")
    request = build_calculate_earnings_request("bronze", test_activity_log)

    assert bool(request) is False
    assert request.parameters == {"tier": "bronze", "activity_log": test_activity_log}
    assert request.error == {
        "parameter": "activity_log",
        "message": f"Invalid format for activity: {test_activity_log[0]}",
        "error_code": error_codes.INVALID_ACTIVITY,
    }


def test_calculate_earnings_request_missing_key_attempt_date_time(test_activity_log):
    test_activity_log[0].pop("attempt_date_time")
    request = build_calculate_earnings_request("bronze", test_activity_log)

    assert bool(request) is False
    assert request.parameters == {"tier": "bronze", "activity_log": test_activity_log}
    assert request.error == {
        "parameter": "activity_log",
        "message": f"Invalid format for activity: {test_activity_log[0]}",
        "error_code": error_codes.INVALID_ACTIVITY,
    }


def test_calculate_earnings_request_missing_key_success(test_activity_log):
    test_activity_log[0].pop("success")
    request = build_calculate_earnings_request("bronze", test_activity_log)

    assert bool(request) is False
    assert request.parameters == {"tier": "bronze", "activity_log": test_activity_log}
    assert request.error == {
        "parameter": "activity_log",
        "message": f"Invalid format for activity: {test_activity_log[0]}",
        "error_code": error_codes.INVALID_ACTIVITY,
    }


def test_calculate_earnings_request_invalid_date_format(test_activity_log):
    test_activity_log[0]["attempt_date_time"] = "2024-01-08AAA15:00:00.000"
    request = build_calculate_earnings_request("bronze", test_activity_log)

    assert bool(request) is False
    assert request.parameters == {"tier": "bronze", "activity_log": test_activity_log}
    assert request.error == {
        "parameter": "activity_log",
        "message": f"Invalid format for activity date: {test_activity_log[0]}",
        "error_code": error_codes.INVALID_ACTIVITY,
    }
