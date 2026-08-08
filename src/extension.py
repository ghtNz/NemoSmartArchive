"""
NemoSmartArchive application bridge.
"""

from pathlib import Path

from src.backends.sevenzip import SevenZipBackend
from src.engine.archive_engine import ArchiveEngine
from src.services.extraction_service import ExtractionService
from src.models.archive import (
    ExtractionResult,
    ExtractionStatus,
)
from src.models.errors import ArchiveReadError
from src.ui.notify import notify


def extract_smart(
    file_path: Path,
):
    """
    Smart extraction entry point.
    """

    backend = SevenZipBackend()

    try:
        archive_info = backend.list(
            file_path
        )

    except ArchiveReadError as error:
        message = str(error)

        notify(
            "NemoSmartArchive",
            message,
        )

        return ExtractionResult(
            status=ExtractionStatus.FAILED,
            output=file_path.parent,
            error=message,
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