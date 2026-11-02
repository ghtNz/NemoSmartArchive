"""
NemoSmartArchive application bridge.
"""

from pathlib import Path

from src.backends.sevenzip import SevenZipBackend
from src.backends.unrar import UnrarBackend
from src.engine.archive_engine import ArchiveEngine
from src.models.archive import (
    ExtractionResult,
    ExtractionStatus,
)
from src.models.errors import ExtractionError
from src.services.extraction_service import ExtractionService
from src.ui.notify import notify


def is_supported_archive(file_path: Path) -> bool:
    """Return whether the file is supported by an archive backend."""
    return SevenZipBackend.is_supported(file_path) or UnrarBackend.is_supported(
        file_path
    )


def extract_smart(
    file_path: Path,
    destination: Path | None = None,
    notify_result: bool = True,
) -> ExtractionResult:
    """Smart extraction entry point."""

    destination = destination if destination is not None else file_path.parent

    if UnrarBackend.is_supported(file_path):
        backend = UnrarBackend()
    else:
        backend = SevenZipBackend()

    try:
        archive_info = backend.list(file_path)

        engine = ArchiveEngine()
        decision = engine.analyze(archive_info)

        service = ExtractionService(backend)

        return service.extract(
            file_path,
            destination,
            decision,
            notify_result=notify_result,
        )

    except ExtractionError as error:
        message = str(error)

        if notify_result:
            notify(
                "NemoSmartArchive",
                message,
            )

        return ExtractionResult(
            status=ExtractionStatus.FAILED,
            output=destination,
            error=message,
        )


def extract_many_smart(
    archives: list[Path],
    destination: Path | None = None,
) -> list[ExtractionResult]:
    """Extract multiple archives and send one summary notification."""

    results = []

    for archive in archives:
        try:
            result = extract_smart(
                archive,
                destination,
                notify_result=False,
            )

        except Exception as error:
            result = ExtractionResult(
                status=ExtractionStatus.FAILED,
                output=destination if destination is not None else archive.parent,
                error=str(error),
            )

        results.append(result)

    successful = sum(result.status == ExtractionStatus.SUCCESS for result in results)

    failed = len(results) - successful

    summary = (
        f"{len(results)} archives processed\n{successful} successful\n{failed} failed"
    )

    if failed:
        failed_names = [
            archive.name
            for archive, result in zip(archives, results)
            if result.status == ExtractionStatus.FAILED
        ]

        summary += "\n\nFailed archives:\n"
        summary += "\n".join(f"- {name}" for name in failed_names)

    notify(
        "NemoSmartArchive",
        summary,
    )

    return results
