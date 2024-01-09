import json
import os

import boto3
import pytest
from moto import mock_secretsmanager

TESTSECRET_NAME = "testsecret"
TESTSECRET_KEY = "testkey"


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


@pytest.fixture(scope="function")
def secretsmanager(aws_credentials):
    # Moto and pytest do not get along too well. See
    # https://github.com/spulec/moto/issues/620
    mocked_secretsmanager = mock_secretsmanager()
    mocked_secretsmanager.start()

    with mock_secretsmanager():
        secretsmanager = boto3.client("secretsmanager")

    secret_value = json.dumps({"api_keys": [TESTSECRET_KEY]})

    secretsmanager.create_secret(Name=TESTSECRET_NAME, SecretString=secret_value)

    yield

    mocked_secretsmanager.stop()
