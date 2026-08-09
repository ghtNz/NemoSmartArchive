"""
Project exceptions.
"""


class ArchiveError(Exception):
    """Base archive exception."""


class BackendNotFoundError(ArchiveError):
    """No supported backend found."""


class ExtractionError(ArchiveError):
    """Extraction failed."""


class TestArchiveError(ArchiveError):
    """Archive test failed."""
