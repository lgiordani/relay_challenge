import os

import pytest
from flask.testing import FlaskClient

from src.application.app import create_app

TEST_API_KEY = "TestApiKey"


@pytest.fixture
def app():
    os.environ["RELAY_API_KEYS_VAULT_TYPE"] = "MEMORY"
    os.environ["RELAY_API_KEY"] = TEST_API_KEY

    app = create_app("testing")

    return app


class TestClient(FlaskClient):
    """
    Extends the default client providing the json kwarg,
    and auto setting the content type, if it is supplied
    """

    def open(self, *args, **kwargs):
        headers = kwargs.get("headers", {})
        headers.setdefault("RELAY-API-KEY", TEST_API_KEY)

        kwargs["headers"] = headers

        return super(TestClient, self).open(*args, **kwargs)


@pytest.fixture
def client(app):
    app.test_client_class = TestClient
    return app.test_client()
