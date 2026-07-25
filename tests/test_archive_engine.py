from pathlib import Path

from src.backends.sevenzip import SevenZipBackend
from src.engine.archive_engine import ArchiveEngine
from src.models.archive import ExtractDecision


def test_single_folder_archive():

    backend = SevenZipBackend()

    info = backend.list(
        Path(
            "tests/data/single_folder.zip"
        )
    )

    engine = ArchiveEngine()

    decision = engine.analyze(info)

    assert decision == (
        ExtractDecision.EXTRACT_HERE
    )


def test_loose_files_archive():

    backend = SevenZipBackend()

    info = backend.list(
        Path(
            "tests/data/loose_files.zip"
        )
    )

    engine = ArchiveEngine()

    decision = engine.analyze(info)

    assert decision == (
        ExtractDecision.CREATE_FOLDER
    )