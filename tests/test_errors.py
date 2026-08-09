import pytest

from pathlib import Path
from src.models.errors import (
    ArchiveReadError,
    ExtractionError,
    PasswordRequiredError,
    UnsupportedArchiveError,
    BackendUnavailableError,
)
from src.models.archive import ExtractionStatus
from src.extension import extract_smart

def test_extraction_error():

    with pytest.raises(ExtractionError):
        raise ExtractionError(
            "test error"
        )

def test_password_error():

    error = PasswordRequiredError(
        "Password required"
    )

    assert str(error) == (
        "Password required"
    )

def test_extract_smart():
    result = extract_smart(
        Path("tests/data/corrupt.zip")
    )
   
    assert result.status == ExtractionStatus.FAILED
    assert result.error == "Unexpected end of archive"

def test_unsupported_archive_error():
    error = UnsupportedArchiveError(
        "Unsupported archive format"
    )

    assert str(error) == "Unsupported archive format"
    assert isinstance(error, ExtractionError)

def test_backend_unavailable_error():
    error = BackendUnavailableError(
        "7-Zip executable not found."
    )

    assert str(error) == "7-Zip executable not found."
    assert isinstance(error, ExtractionError)