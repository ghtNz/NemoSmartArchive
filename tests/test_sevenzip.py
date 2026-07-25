from src.backends.sevenzip import SevenZipBackend


def test_backend_exists():
    backend = SevenZipBackend()

    assert backend.is_available()