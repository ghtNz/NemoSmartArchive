"""
Archive data models.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from enum import Enum

class ExtractDecision(Enum):
    """Smart extraction decision."""

    EXTRACT_HERE = "extract_here"
    CREATE_FOLDER = "create_folder"

class ExtractionStatus(Enum):
    """Extraction result state."""

    SUCCESS = "success"
    FAILED = "failed"

@dataclass(frozen=True)
class ArchiveEntry:
    """Single archive item."""

    name: str
    is_directory: bool

@dataclass(frozen=True)
class ArchiveInfo:
    """Information about an archive."""

    path: Path
    entries: list[ArchiveEntry]

@dataclass(frozen=True)
class ExtractionResult:
    """Result returned after extraction."""

    status: ExtractionStatus
    output: Path
    error: str | None = None