import os

from flask import Flask


def create_app(config_name):
    config_module = f"src.application.config.{config_name.capitalize()}Config"

    app = Flask(__name__)

    app.config.from_object(config_module)

    # Configure the vault

    vault_type = app.config["API_KEYS_VAULT_TYPE"]

    if vault_type == "SECRETSMANAGER":
        from src.vault.secretsmanager_vault import SecretsManagerVault

        app.config["VAULT"] = SecretsManagerVault(app.config["API_KEYS_VAULT_NAME"])

    elif vault_type == "MEMORY":
        from src.vault.memory_vault import MemoryVault

        app.config["VAULT"] = MemoryVault(app.config["API_KEY"])
    else:
        raise ValueError(f"Unsupported vault type: {vault_type}")

    from src.application.routes import route_blueprint

    app.register_blueprint(route_blueprint)

    return app
