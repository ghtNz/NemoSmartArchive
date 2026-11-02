from pathlib import Path

import pytest

from src.backends.unrar import UnrarBackend
from src.models.errors import (
    ArchiveReadError,
    BackendUnavailableError,
    UnsupportedArchiveError,
)

RAR_ARCHIVE = Path("tests/data/test.rar")


def test_backend_exists():
    backend = UnrarBackend()

    assert backend.is_available()


def test_version():
    backend = UnrarBackend()

    assert "UNRAR" in backend.version()


def test_supported_extensions():
    supported = (
        "test.rar",
        "TEST.RAR",
    )

    for filename in supported:
        assert UnrarBackend.is_supported(Path(filename))


def test_unsupported_extension():
    unsupported = (
        "test.zip",
        "test.7z",
        "photo.jpg",
        "document.pdf",
    )

    for filename in unsupported:
        assert not UnrarBackend.is_supported(Path(filename))


def test_list_archive():
    backend = UnrarBackend()

    info = backend.list(RAR_ARCHIVE)

    assert len(info.entries) == 70
    assert sum(not entry.is_directory for entry in info.entries) == 69
    assert sum(entry.is_directory for entry in info.entries) == 1


def test_archive_integrity():
    backend = UnrarBackend()

    assert backend.test(RAR_ARCHIVE) is True


def test_extract_archive(tmp_path):
    backend = UnrarBackend()

    backend.extract(RAR_ARCHIVE, tmp_path)

    extracted_files = list(tmp_path.rglob("*"))

    assert len(extracted_files) > 0


def test_missing_archive():
    backend = UnrarBackend()

    with pytest.raises(ArchiveReadError):
        backend.list(Path("tests/data/missing.rar"))


def test_missing_archive_extract(tmp_path):
    backend = UnrarBackend()

    with pytest.raises(ArchiveReadError):
        backend.extract(
            Path("tests/data/missing.rar"),
            tmp_path,
        )


def test_unsupported_archive():
    backend = UnrarBackend()

    with pytest.raises(UnsupportedArchiveError):
        backend.list(Path("tests/data/photo.jpg"))


def test_backend_unavailable():
    backend = UnrarBackend()
    backend._binary = None

    with pytest.raises(BackendUnavailableError):
        _ = backend.binary
