from typing import Optional


class Request:
    def __init__(self, parameters: Optional[dict] = None, error: Optional[dict] = None):
        self.parameters = parameters or {}
        self.error = error or {}

    def __bool__(self):
        return True

    def __repr__(self):
        return f"{self.__class__.__name__} - {self.parameters} - {self.error}"


class ValidRequest(Request):
    pass


class InvalidRequest(Request):
    def __init__(
        self, parameter, error_code, message, request_parameters: Optional[dict] = None
    ):
        error = {"parameter": parameter, "error_code": error_code, "message": message}
        super().__init__(request_parameters, error)

    def __bool__(self):
        return False
