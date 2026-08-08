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

    info = backend.list(
        Path("tests/data/loose_files.zip")
    )

    assert len(info.entries) > 0


def test_supported_extensions():
    supported = (
        "test.zip",
        "test.7z",
        "test.tar",
        "test.tar.gz",
        "test.tgz",
        "test.tar.bz2",
        "test.tar.xz",
    )

    for filename in supported:
        assert SevenZipBackend.is_supported(
            Path(filename)
        )


def test_unsupported_extension():
    unsupported = (
        "photo.jpg",
        "document.pdf",
        "video.mp4",
        "README.md",
    )

    for filename in unsupported:
        assert not SevenZipBackend.is_supported(
            Path(filename)
        )

def test_archive_integrity():
    backend = SevenZipBackend()

    result = backend.test(
        Path("tests/data/loose_files.zip")
    )

    assert result is True

def test_corrupt_archive_integrity():
    backend = SevenZipBackend()

    result = backend.test(
        Path("tests/data/corrupt.zip")
    )

    assert result is False