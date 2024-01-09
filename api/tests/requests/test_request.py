from src.requests.request import InvalidRequest, ValidRequest


def test_valid_request():
    parameters = {"key1": "value1", "key2": "value2"}
    request = ValidRequest(parameters)

    assert bool(request) is True
    assert request.parameters == parameters
    assert str(request) == "ValidRequest - {'key1': 'value1', 'key2': 'value2'} - {}"


def test_valid_request_without_parameters():
    request = ValidRequest()

    assert bool(request) is True
    assert request.parameters == {}


def test_invalid_request():
    parameters = {"key1": "value1", "key2": "value2"}
    request = InvalidRequest("key1", "TEST_CODE", "TEST_MESSAGE", parameters)

    assert bool(request) is False
    assert request.parameters == parameters
    assert request.error == {
        "parameter": "key1",
        "error_code": "TEST_CODE",
        "message": "TEST_MESSAGE",
    }
    assert str(request) == (
        "InvalidRequest - {'key1': 'value1', 'key2': 'value2'} "
        "- {'parameter': 'key1', 'error_code': 'TEST_CODE', 'message': 'TEST_MESSAGE'}"
    )


def test_invalid_request_without_parameters():
    request = InvalidRequest("key1", "TEST_CODE", "TEST_MESSAGE")

    assert bool(request) is False
    assert request.parameters == {}
    assert request.error == {
        "parameter": "key1",
        "error_code": "TEST_CODE",
        "message": "TEST_MESSAGE",
    }
