import json

import boto3

from src.vault.vault import Vault


class SecretsManagerVault(Vault):
    def __init__(self, secret_name):
        secret = boto3.client("secretsmanager").get_secret_value(SecretId=secret_name)
        secret_dict = json.loads(secret["SecretString"])

        self.keys = secret_dict["api_keys"]

    def get_keys(self) -> list[str]:
        return self.keys

    def check_key(self, key: str) -> bool:
        return key in self.keys
