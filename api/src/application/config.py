import os


class Config:
    """Base configuration"""

    # API Keys Vault configuration

    # This is the type of the API Keys Vault
    API_KEYS_VAULT_TYPE = os.environ.get("RELAY_API_KEYS_VAULT_TYPE")

    # This is the value of the Secrets Manager secret (if any) for the API key
    API_KEYS_VAULT_NAME = os.environ.get("RELAY_API_KEYS_VAULT_NAME")

    # This is the value of the API key if not passed throught the vault
    API_KEY = os.environ.get("RELAY_API_KEY", "development-key")


class LiveConfig(Config):
    """Live configuration"""


class DevelopmentConfig(Config):
    """Development configuration"""


class TestingConfig(Config):
    """Testing configuration"""

    TESTING = True
