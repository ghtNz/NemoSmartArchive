"""
Application-specific exceptions.
"""

class ExtractionError(Exception):
    """Raised when archive extraction fails."""

    pass

class PasswordRequiredError(ExtractionError):
    """Archive requires a password."""

    pass