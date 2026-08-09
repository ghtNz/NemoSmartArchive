from pathlib import Path

from src.backends.sevenzip import SevenZipBackend
from src.services.extraction_service import ExtractionService
from src.models.archive import (
    ExtractDecision,
    ExtractionStatus,
)
from src.models.errors import ExtractionError


def test_extract_loose_files(tmp_path):

    archive = Path(
        "tests/data/loose_files.zip"
    )

    service = ExtractionService()

    result = service.extract(
        archive,
        tmp_path,
        ExtractDecision.CREATE_FOLDER,
    )

    assert result.status.value == "success"

    assert (
        result.output /
        "file1.txt"
    ).exists()

def test_corrupt_archive_is_rejected(tmp_path):
    archive = Path(
        "tests/data/corrupt.zip"
    )

    service = ExtractionService()

    result = service.extract(
        archive,
        tmp_path,
        ExtractDecision.CREATE_FOLDER,
    )

    assert result.status == ExtractionStatus.FAILED
    assert result.error == "Archive integrity check failed."

def test_password_protected_archive_is_rejected(tmp_path):
    archive = Path(
        "tests/data/password.zip"
    )

    service = ExtractionService()

    result = service.extract(
        archive,
        tmp_path,
        ExtractDecision.EXTRACT_HERE,
    )

    assert result.status == ExtractionStatus.FAILED
    assert result.error == "Archive password required"

def test_unsupported_archive_is_rejected(tmp_path):
    archive = Path(
        "tests/data/photo.jpg"
    )

    service = ExtractionService()

    result = service.extract(
        archive,
        tmp_path,
        ExtractDecision.EXTRACT_HERE,
    )

    assert result.status == ExtractionStatus.FAILED
    assert result.error == (
        "Unsupported archive format: photo.jpg"
    )

def test_missing_archive_is_rejected(tmp_path):
    archive = Path(
        "tests/data/missing.zip"
    )

    service = ExtractionService()

    result = service.extract(
        archive,
        tmp_path,
        ExtractDecision.EXTRACT_HERE,
    )

    assert result.status == ExtractionStatus.FAILED
    assert result.error == (
        "Archive not found: tests/data/missing.zip"
    )

def test_backend_unavailable_is_rejected(tmp_path):
    archive = Path(
        "tests/data/loose_files.zip"
    )

    backend = SevenZipBackend()
    backend._binary = None

    service = ExtractionService(
        backend
    )

    result = service.extract(
        archive,
        tmp_path,
        ExtractDecision.EXTRACT_HERE,
    )

    assert result.status == ExtractionStatus.FAILED
    assert result.error == (
        "7-Zip executable not found."
    )

def test_extract_creates_archive_folder(tmp_path):
    archive = Path(
        "tests/data/loose_files.zip"
    )

    service = ExtractionService()

    result = service.extract(
        archive,
        tmp_path,
        ExtractDecision.CREATE_FOLDER,
    )

    expected = tmp_path / "loose_files"

    assert result.status == ExtractionStatus.SUCCESS
    assert result.output == expected
    assert expected.is_dir()
    assert (expected / "file1.txt").is_file()
    assert (expected / "file2.txt").is_file()

def test_extraction_error_is_rejected(tmp_path):
    class FailingBackend:
        def test(self, archive):
            return True

        def extract(self, archive, destination):
            raise ExtractionError(
                "Extraction failed"
            )

    service = ExtractionService(
        FailingBackend()
    )

    result = service.extract(
        Path("tests/data/loose_files.zip"),
        tmp_path,
        ExtractDecision.EXTRACT_HERE,
    )

    assert result.status == ExtractionStatus.FAILED
    assert result.error == "Extraction failed"

def test_integrity_failure_is_rejected_without_extraction(
    tmp_path,
):
    class InvalidBackend:
        def test(self, archive):
            return False

        def extract(self, archive, destination):
            raise AssertionError(
                "extract() should not be called"
            )

    service = ExtractionService(
        InvalidBackend()
    )

    result = service.extract(
        Path("tests/data/loose_files.zip"),
        tmp_path,
        ExtractDecision.EXTRACT_HERE,
    )

    assert result.status == ExtractionStatus.FAILED
    assert result.error == (
        "Archive integrity check failed."
    )
