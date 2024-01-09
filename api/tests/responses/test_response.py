from src.requests.request import InvalidRequest
from src.responses.response import (
    ResponseFailure,
    ResponseSuccess,
    build_response_from_invalid_request,
)

SUCCESS_VALUE = {"key": ["value1", "value2"]}
TEST_CODE = "Error"
TEST_MESSAGE = "This is a response"


def test_response_success_is_true():
    response = ResponseSuccess(SUCCESS_VALUE)

    assert bool(response) is True


def test_response_failure_is_false():
    response = ResponseFailure(TEST_CODE, TEST_MESSAGE)

    assert bool(response) is False


def test_response_success_has_value():
    response = ResponseSuccess(SUCCESS_VALUE)

    assert response.value == SUCCESS_VALUE


def test_response_failure_has_message():
    response = ResponseFailure(TEST_CODE, TEST_MESSAGE)

    assert response.error_code == TEST_CODE
    assert response.message == TEST_MESSAGE
    assert response.value == {
        "error_code": TEST_CODE,
        "message": TEST_MESSAGE,
    }


def test_response_failure_has_repr():
    response = ResponseFailure(TEST_CODE, TEST_MESSAGE)

    assert str(response) == f"ResponseFailure [{TEST_CODE}] - {TEST_MESSAGE}"


def test_response_failure_initialisation_with_exception():
    response = ResponseFailure(TEST_CODE, Exception("Just an error message"))

    assert bool(response) is False
    assert response.message == "Exception: Just an error message"


def test_response_failure_from_empty_invalid_request():
    request = InvalidRequest("TEST_PARAMETER", "TEST_CODE", "TEST_MESSAGE")

    response = build_response_from_invalid_request(request)

    assert bool(response) is False
    assert response.error_code == "TEST_CODE"
    assert response.message == "TEST_PARAMETER: TEST_MESSAGE"
