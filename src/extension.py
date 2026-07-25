"""
NemoSmartArchive application bridge.
"""

from pathlib import Path

from src.backends.sevenzip import SevenZipBackend
from src.engine.archive_engine import ArchiveEngine
from src.services.extraction_service import ExtractionService


def extract_smart(
    file_path: Path,
):
    """
    Smart extraction entry point.
    """

    backend = SevenZipBackend()

    archive_info = backend.list(
        file_path
    )

    engine = ArchiveEngine()

    decision = engine.analyze(
        archive_info
    )

    service = ExtractionService(
        backend
    )

    return service.extract(
        file_path,
        file_path.parent,
        decision,
    )