from http import HTTPStatus
from unittest.mock import Mock, patch

from src.responses.response import ResponseFailure, ResponseSuccess

from src.use_cases import error_codes


@patch("src.application.routes.build_calculate_earnings_request")
@patch("src.application.routes.calculate_earnings_use_case")
def test_calculate_earnings(
    mock_calculate_earnings_use_case,
    mock_build_calculate_earnings_request,
    app,
    client,
    test_activity_log,
):
    earnings = {"test": "earnings"}

    mock_calculate_earnings_use_case.return_value = ResponseSuccess(earnings)

    api_response = client.post(
        "/earnings/bronze", json=test_activity_log, content_type="application/json"
    )

    assert api_response.status_code == HTTPStatus.CREATED
    mock_build_calculate_earnings_request.assert_called_with(
        "bronze", test_activity_log
    )
    mock_calculate_earnings_use_case.assert_called_with(
        mock_build_calculate_earnings_request.return_value
    )

    assert api_response.json == earnings


@patch("src.application.routes.calculate_earnings_use_case")
def test_calculate_earnings_missing_parameters(
    mock_calculate_earnings_use_case, app, client, test_activity_log
):
    message = "some-message"

    mock_calculate_earnings_use_case.return_value = ResponseFailure(
        error_codes.MISSING_PARAMETERS,
        message,
    )
    api_response = client.post(
        "/earnings/bronze", json=test_activity_log, content_type="application/json"
    )

    assert api_response.status_code == HTTPStatus.BAD_REQUEST
    assert api_response.json == {
        "code": error_codes.MISSING_PARAMETERS,
        "message": message,
    }


@patch("src.application.routes.calculate_earnings_use_case")
def test_create_generic_error(
    mock_calculate_earnings_use_case, app, client, test_activity_log
):
    error_code = "error-code"
    message = "some-message"

    mock_calculate_earnings_use_case.return_value = ResponseFailure(
        error_code,
        message,
    )

    api_response = client.post(
        "/earnings/bronze", json=test_activity_log, content_type="application/json"
    )

    assert api_response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert api_response.json == {"code": error_code, "message": message}
