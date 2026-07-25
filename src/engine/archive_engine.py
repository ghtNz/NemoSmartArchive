from pathlib import Path


class ArchiveEngine:
    """Archive operations."""

    SUPPORTED_EXTENSIONS = {
        ".zip",
        ".7z",
        ".rar",
        ".tar",
        ".gz",
        ".bz2",
        ".xz",
    }

    @classmethod
    def is_supported(cls, path: str) -> bool:
        suffixes = Path(path).suffixes

        if not suffixes:
            return False

        full = "".join(suffixes).lower()

        if full in (
            ".tar.gz",
            ".tar.bz2",
            ".tar.xz",
        ):
            return True

        return suffixes[-1].lower() in cls.SUPPORTED_EXTENSIONS
