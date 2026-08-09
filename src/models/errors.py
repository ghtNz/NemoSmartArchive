"""
Application-specific exceptions.
"""

class ExtractionError(Exception):
    """Raised when archive extraction fails."""

    pass

class PasswordRequiredError(ExtractionError):
    """Archive requires a password."""

    pass

class ArchiveReadError(ExtractionError):
    """Raised when an archive cannot be read or inspected."""

    pass

class UnsupportedArchiveError(ExtractionError):
    """Raised when the archive format is not supported."""
    pass

class BackendUnavailableError(ExtractionError):
    """Raised when the required archive backend is unavailable."""
    pass
