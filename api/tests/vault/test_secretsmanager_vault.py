from src.vault.secretsmanager_vault import SecretsManagerVault
from tests.vault.conftest import TESTSECRET_KEY, TESTSECRET_NAME


def test_secretsmanager_vault(secretsmanager):
    sm_vault = SecretsManagerVault(TESTSECRET_NAME)

    assert sm_vault.get_keys() == [TESTSECRET_KEY]


def test_secretsmanager_vault_check_key(secretsmanager):
    sm_vault = SecretsManagerVault(TESTSECRET_NAME)

    assert sm_vault.check_key(TESTSECRET_KEY) is True
    assert sm_vault.check_key("random") is False
