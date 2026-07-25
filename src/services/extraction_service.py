"""
Extraction workflow service.
"""

from __future__ import annotations

from pathlib import Path

from src.backends.sevenzip import SevenZipBackend
from src.models.archive import (
    ExtractDecision,
    ExtractionResult,
    ExtractionStatus,
)

from src.models.errors import ExtractionError


class ExtractionService:
    """Handle archive extraction workflow."""

    def __init__(
        self,
        backend: SevenZipBackend | None = None,
    ):
        self.backend = backend or SevenZipBackend()

    def extract(
        self,
        archive: Path,
        destination: Path,
        decision: ExtractDecision,
    ) -> ExtractionResult:
        """
        Extract archive according to decision.
        """

        if decision == ExtractDecision.CREATE_FOLDER:
            output = destination / archive.stem

        else:
            output = destination

        try:

            self.backend.extract(
                archive,
                output,
            )

            return ExtractionResult(
                status=ExtractionStatus.SUCCESS,
                output=output,
            )

        except ExtractionError as error:

            return ExtractionResult(
                status=ExtractionStatus.FAILED,
                output=output,
                error=str(error),
            )