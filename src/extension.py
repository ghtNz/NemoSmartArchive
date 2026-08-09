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
from src.models.errors import ExtractionError
from src.ui.notify import notify


def extract_smart(
    file_path: Path,
    destination: Path | None = None,
):
    """
    Smart extraction entry point.
    """

    destination = (
        destination
        if destination is not None
        else file_path.parent
    )

    backend = SevenZipBackend()

    try:
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
            destination,
            decision,
        )

    except ExtractionError as error:
        message = str(error)

        notify(
            "NemoSmartArchive",
            message,
        )

        return ExtractionResult(
            status=ExtractionStatus.FAILED,
            output=destination,
            error=message,
        )
