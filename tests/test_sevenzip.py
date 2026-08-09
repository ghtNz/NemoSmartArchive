import pytest

from pathlib import Path
from src.backends.sevenzip import SevenZipBackend
from src.models.errors import (
    ArchiveReadError,
    ExtractionError,
    PasswordRequiredError,
    UnsupportedArchiveError,
    BackendUnavailableError,
)


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

def test_password_protected_archive():
    backend = SevenZipBackend()

    with pytest.raises(
        PasswordRequiredError,
        match="Archive password required",
    ):
        backend.extract(
            Path("tests/data/password.zip"),
            Path("/tmp/nemosmartarchive-password-test"),
        )

def test_unsupported_archive_is_rejected():
    backend = SevenZipBackend()

    with pytest.raises(UnsupportedArchiveError):
        backend.list(
            Path("tests/data/photo.jpg")
        )

def test_unsupported_archive_extract_is_rejected(
    tmp_path,
):
    backend = SevenZipBackend()

    with pytest.raises(UnsupportedArchiveError):
        backend.extract(
            Path("tests/data/photo.jpg"),
            tmp_path,
        )

def test_missing_archive_is_rejected():
    backend = SevenZipBackend()

    with pytest.raises(ArchiveReadError):
        backend.list(
            Path("tests/data/missing.zip")
        )

def test_missing_archive_extract_is_rejected(
    tmp_path,
):
    backend = SevenZipBackend()

    with pytest.raises(ArchiveReadError):
        backend.extract(
            Path("tests/data/missing.zip"),
            tmp_path,
        )

def test_backend_unavailable():
    backend = SevenZipBackend()

    backend._binary = None

    with pytest.raises(BackendUnavailableError):
        _ = backend.binary

def test_unsupported_archive_integrity_is_rejected():
    backend = SevenZipBackend()

    with pytest.raises(UnsupportedArchiveError):
        backend.test(
            Path("tests/data/photo.jpg")
        )

def test_missing_archive_integrity_is_rejected():
    backend = SevenZipBackend()

    with pytest.raises(ArchiveReadError):
        backend.test(
            Path("tests/data/missing.zip")
        )