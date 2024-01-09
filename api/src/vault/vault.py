class VaultError(ValueError):
    """A generic Vault error"""


class Vault:
    def get_keys(self) -> list[str]:
        raise NotImplementedError  # pragma: no cover

    def check_key(self, key: str) -> bool:
        raise NotImplementedError  # pragma: no cover
