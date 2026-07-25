import pytest

from src.models.errors import  (
    ExtractionError,
    PasswordRequiredError,
)

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