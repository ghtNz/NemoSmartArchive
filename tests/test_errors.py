import pytest

from pathlib import Path
from src.models.errors import  (
    ExtractionError,
    PasswordRequiredError,
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