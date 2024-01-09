from src.vault.vault import Vault


class MemoryVault(Vault):
    def __init__(self, key):
        self.key = key

    def get_keys(self) -> list[str]:
        return [self.key]

    def check_key(self, key: str) -> bool:
        return key == self.key
