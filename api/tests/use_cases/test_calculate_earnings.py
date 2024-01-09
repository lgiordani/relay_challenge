# from unittest import mock

# from src.datastore.datastore import DatastoreError, UserAlreadyExists
# from src.requests.request import InvalidRequest
# from src.use_cases import error_codes
# from src.use_cases.calculate_earnings import (
#     build_calculate_earnings_request,
#     calculate_earnings_use_case,
# )


# def test_calculate_earnings(test_activity_log):
#     request = build_calculate_earnings_request(test_activity_log)

#     response = calculate_earnings_use_case(request)

#     assert bool(response) is True
#     assert response.value == test_user["user_id"]

#     datastore.calculate_earnings.assert_called_with(
#         test_user["user_id"],
#         email=test_user["email"],
#         password=test_user["password"],
#         otp_secret=None,
#     )


# @mock.patch("src.use_cases.calculate_earnings.email_formatter")
# def test_calculate_earnings_calls_email_formatter(
#     mock_email_formatter, test_user, user_entity
# ):
#     datastore = mock.Mock()

#     request = build_calculate_earnings_request(
#         email=test_user["email"],
#         user_id=test_user["user_id"],
#         password=test_user["password"],
#     )

#     response = calculate_earnings_use_case(datastore, request)

#     assert bool(response) is True

#     mock_email_formatter.assert_called_with(test_user["email"], validator=None)
#     datastore.calculate_earnings.assert_called_with(
#         test_user["user_id"],
#         email=mock_email_formatter.return_value,
#         password=test_user["password"],
#         otp_secret=None,
#     )


# @mock.patch("src.use_cases.calculate_earnings.email_formatter")
# def test_calculate_earnings_calls_email_formatter_with_validator(
#     mock_email_formatter, test_user, user_entity
# ):
#     email_validator = mock.Mock()

#     datastore = mock.Mock()

#     request = build_calculate_earnings_request(
#         email=test_user["email"],
#         user_id=test_user["user_id"],
#         password=test_user["password"],
#     )

#     response = calculate_earnings_use_case(datastore, request, email_validator=email_validator)

#     assert bool(response) is True

#     mock_email_formatter.assert_called_with(
#         test_user["email"], validator=email_validator
#     )


# @mock.patch("src.use_cases.calculate_earnings.generate_uuid")
# def test_calculate_earnings_without_user_id(mock_generate_uuid, test_user, user_entity):
#     datastore = mock.Mock()
#     datastore.calculate_earnings.return_value = user_entity

#     request = build_calculate_earnings_request(
#         email=test_user["email"], password=test_user["password"]
#     )

#     response = calculate_earnings_use_case(datastore, request)

#     assert bool(response) is True

#     datastore.calculate_earnings.assert_called_with(
#         mock_generate_uuid.return_value,
#         email=test_user["email"],
#         password=test_user["password"],
#         otp_secret=None,
#     )


# @mock.patch("src.use_cases.calculate_earnings.generate_uuid")
# def test_calculate_earnings_with_user_id_is_none(mock_generate_uuid, test_user, user_entity):
#     datastore = mock.Mock()
#     datastore.calculate_earnings.return_value = user_entity

#     request = build_calculate_earnings_request(
#         user_id=None, email=test_user["email"], password=test_user["password"]
#     )

#     response = calculate_earnings_use_case(datastore, request)

#     assert bool(response) is True

#     datastore.calculate_earnings.assert_called_with(
#         mock_generate_uuid.return_value,
#         email=test_user["email"],
#         password=test_user["password"],
#         otp_secret=None,
#     )


# def test_calculate_earnings_with_otp(test_user, user_entity):
#     datastore = mock.Mock()
#     datastore.calculate_earnings.return_value = user_entity

#     request = build_calculate_earnings_request(
#         email=test_user["email"],
#         user_id=test_user["user_id"],
#         password=test_user["password"],
#         otp_secret=test_user["otp_secret"],
#     )

#     response = create_user_use_case(datastore, request)

#     assert bool(response) is True

#     datastore.create_user.assert_called_with(
#         test_user["user_id"],
#         email=test_user["email"],
#         password=test_user["password"],
#         otp_secret=test_user["otp_secret"],
#     )


# def test_create_user_without_password(test_user, user_entity):
#     datastore = mock.Mock()
#     datastore.create_user.return_value = user_entity

#     request = build_create_user_request(
#         email=test_user["email"], user_id=test_user["user_id"]
#     )

#     response = create_user_use_case(datastore, request)

#     assert bool(response) is True

#     datastore.create_user.assert_called_with(
#         test_user["user_id"],
#         email=test_user["email"],
#         password=None,
#         otp_secret=None,
#     )


# def test_create_user_already_exists(test_user, user_entity):
#     datastore = mock.Mock()
#     datastore.create_user.side_effect = UserAlreadyExists

#     request = build_create_user_request(
#         email=test_user["email"],
#         user_id=test_user["user_id"],
#         password=test_user["password"],
#     )

#     response = create_user_use_case(datastore, request)

#     assert bool(response) is False

#     datastore.create_user.assert_called_with(
#         test_user["user_id"],
#         email=test_user["email"],
#         password=test_user["password"],
#         otp_secret=None,
#     )
#     assert response.error_code == error_codes.USER_ALREADY_EXISTS


# def test_create_user_invalid_email(test_user, user_entity):
#     email_validator = mock.Mock()
#     email_validator.side_effect = ValueError

#     datastore = mock.Mock()

#     request = build_create_user_request(
#         email=test_user["email"],
#         user_id=test_user["user_id"],
#         password=test_user["password"],
#     )

#     response = create_user_use_case(datastore, request, email_validator=email_validator)

#     assert bool(response) is False
#     assert response.error_code == error_codes.INVALID_CREDENTIALS

#     datastore.create_user.assert_not_called()


# def test_create_user_invalid_request(test_user, user_entity):
#     datastore = mock.Mock()
#     datastore.create_user.return_value = user_entity

#     request = InvalidRequest("key1", "TEST_CODE", "TEST_MESSAGE")

#     response = create_user_use_case(datastore, request)

#     assert bool(response) is False
#     assert response.error_code == "TEST_CODE"

#     datastore.create_user.assert_not_called()


# def test_create_user_datastore_error(test_user, user_entity):
#     datastore = mock.Mock()
#     datastore.create_user.side_effect = DatastoreError

#     request = build_create_user_request(
#         email=test_user["email"],
#         user_id=test_user["user_id"],
#         password=test_user["password"],
#     )

#     response = create_user_use_case(datastore, request)

#     assert bool(response) is False
#     assert response.error_code == error_codes.UNKNOWN_ERROR

#     datastore.create_user.assert_called_with(
#         test_user["user_id"],
#         email=test_user["email"],
#         password=test_user["password"],
#         otp_secret=None,
#     )
