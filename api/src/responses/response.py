class ResponseFailure:
    def __init__(self, error_code, message):
        self.error_code = error_code
        self.message = self._format_message(message)

    def _format_message(self, msg):
        if isinstance(msg, Exception):
            return "{}: {}".format(msg.__class__.__name__, "{}".format(msg))
        return msg

    @property
    def value(self):
        return {
            "error_code": self.error_code,
            "message": self.message,
        }

    def __bool__(self):
        return False

    def __repr__(self):
        return f"{self.__class__.__name__} [{self.error_code}] - {self.message}"


class ResponseSuccess:
    def __init__(self, value=None):
        self.value = value
        self.error_code = None
        self.message = None

    def __bool__(self):
        return True


def build_response_from_invalid_request(invalid_request):
    error = invalid_request.error

    message = f'{error["parameter"]}: {error["message"]}'

    return ResponseFailure(error["error_code"], message)
