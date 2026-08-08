from pathlib import Path

from src.backends.sevenzip import SevenZipBackend
from src.services.extraction_service import ExtractionService
from src.models.archive import (
    ExtractDecision,
    ExtractionStatus,
)


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
