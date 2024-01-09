from src.vault.memory_vault import MemoryVault


def test_memory_vault():
    test_key = "just-a-test-key"
    memory_valut = MemoryVault(test_key)

    assert memory_valut.get_keys() == [test_key]


def test_memory_vault_check_key():
    test_key = "just-a-test-key"
    memory_valut = MemoryVault(test_key)

    assert memory_valut.check_key(test_key) is True
    assert memory_valut.check_key("random") is False
