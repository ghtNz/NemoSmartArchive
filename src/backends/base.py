"""
Abstract interface for archive backends.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from src.models.archive import ArchiveInfo


class ArchiveBackend(ABC):
    """Base interface for archive backends."""

    @abstractmethod
    def is_available(self) -> bool:
        """Return True if the backend is installed."""

    @abstractmethod
    def version(self) -> str:
        """Return backend version."""

    @abstractmethod
    def list(self, archive: Path) -> ArchiveInfo:
        """Return archive contents."""

    @abstractmethod
    def extract(
        self,
        archive: Path,
        destination: Path,
    ) -> None:
        """Extract archive."""

    @abstractmethod
    def test(self, archive: Path) -> bool:
        """Verify archive integrity."""
