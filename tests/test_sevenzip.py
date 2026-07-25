from src.backends.sevenzip import SevenZipBackend
from pathlib import Path


def test_backend_exists():
    backend = SevenZipBackend()

    assert backend.is_available()

def test_version():
    backend = SevenZipBackend()

    version = backend.version()

    assert len(version) > 0
    assert "7-Zip" in version

def test_list_archive():

    backend = SevenZipBackend()

    archive = Path(
        "tests/data/single_folder.zip"
    )

    info = backend.list(archive)

    assert len(info.entries) > 0

    names = [
        entry.name
        for entry in info.entries
    ]

    assert any(
        "image1.jpg" in name
        for name in names
    )