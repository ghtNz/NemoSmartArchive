from src.backends.sevenzip import SevenZipBackend


def test_backend_exists():
    backend = SevenZipBackend()

    assert backend.is_available()

def test_version():
    backend = SevenZipBackend()

    version = backend.version()

    assert len(version) > 0
    assert "7-Zip" in version