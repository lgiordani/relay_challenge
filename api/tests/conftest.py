import random
import string

# from datetime import datetime

import pytest

# from src.entities.earnings_statement import EarningsStatement


def pytest_addoption(parser):
    parser.addoption(
        "--e2e",
        action="store_true",
        default=False,
        help="Run end to end tests (requires a running server on localhost)",
    )


def pytest_collection_modifyitems(config, items):
    # if config.getoption("--e2e"):
    # skipper = pytest.mark.skip(reason="Only run when --e2e is given")
    for item in items:
        if "e2e" in item.nodeid:
            item.add_marker(pytest.mark.e2e)
        else:
            item.add_marker(pytest.mark.unit)


@pytest.fixture(scope="session")
def random_string():
    def _random_string():
        return "".join(
            random.choices(
                string.ascii_lowercase + string.ascii_uppercase + string.digits, k=15
            )
        )

    return _random_string


@pytest.fixture(scope="function")
def test_activity_log():
    return [
        {
            "route_id": "some-route-id",
            "attempt_date_time": "2024-01-08T15:00:00.000",
            "success": True,
        }
    ]


# @pytest.fixture(scope="function")
# def test_web_user(test_user):
#     return {
#         "uuid": test_user["user_id"],
#         "email": test_user["email"],
#         "password": test_user["password"],
#         "otp_secret": test_user["otp_secret"],
#     }


# @pytest.fixture(scope="function")
# def user_entity(test_user):
#     return User(
#         test_user["user_id"],
#         email=test_user["email"],
#         password="hashed-password",
#         password_timestamp=datetime.utcnow().isoformat(),
#         otp_secret=None,
#         otp_enabled=False,
#     )


# @pytest.fixture(scope="function")
# def another_user_entity(test_user):
#     return User(
#         "another-user-id",
#         email="anotheruser@email.com",
#         password="another-password",
#         password_timestamp=datetime.utcnow().isoformat(),
#         otp_secret=None,
#         otp_enabled=False,
#     )
