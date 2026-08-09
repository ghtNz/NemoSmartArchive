from pathlib import Path

from src.backends.sevenzip import SevenZipBackend
from src.engine.archive_engine import ArchiveEngine
from src.models.archive import (
    ArchiveEntry,
    ArchiveInfo,
    ExtractDecision,
)


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

def test_single_file_archive_creates_folder():
    archive = ArchiveInfo(
        path=Path("test.zip"),
        entries=[
            ArchiveEntry(
                name="file.txt",
                is_directory=False,
            )
        ],
    )

    engine = ArchiveEngine()

    assert engine.analyze(archive) == (
        ExtractDecision.CREATE_FOLDER
    )

def test_multiple_top_level_files_create_folder():
    archive = ArchiveInfo(
        path=Path("test.zip"),
        entries=[
            ArchiveEntry(
                name="file1.txt",
                is_directory=False,
            ),
            ArchiveEntry(
                name="file2.txt",
                is_directory=False,
            ),
        ],
    )

    engine = ArchiveEngine()

    assert engine.analyze(archive) == (
        ExtractDecision.CREATE_FOLDER
    )

def test_multiple_top_level_directories_create_folder():
    archive = ArchiveInfo(
        path=Path("test.zip"),
        entries=[
            ArchiveEntry(
                name="folder1/",
                is_directory=True,
            ),
            ArchiveEntry(
                name="folder2/",
                is_directory=True,
            ),
        ],
    )

    engine = ArchiveEngine()

    assert engine.analyze(archive) == (
        ExtractDecision.CREATE_FOLDER
    )

def test_mixed_top_level_entries_create_folder():
    archive = ArchiveInfo(
        path=Path("test.zip"),
        entries=[
            ArchiveEntry(
                name="folder/",
                is_directory=True,
            ),
            ArchiveEntry(
                name="file.txt",
                is_directory=False,
            ),
        ],
    )

    engine = ArchiveEngine()

    assert engine.analyze(archive) == (
        ExtractDecision.CREATE_FOLDER
    )

def test_empty_archive_creates_folder():
    archive = ArchiveInfo(
        path=Path("test.zip"),
        entries=[],
    )

    engine = ArchiveEngine()

    assert engine.analyze(archive) == (
        ExtractDecision.CREATE_FOLDER
    )

def test_nested_files_under_single_directory_extract_here():
    archive = ArchiveInfo(
        path=Path("test.zip"),
        entries=[
            ArchiveEntry(
                name="photos/",
                is_directory=True,
            ),
            ArchiveEntry(
                name="photos/image1.jpg",
                is_directory=False,
            ),
            ArchiveEntry(
                name="photos/image2.jpg",
                is_directory=False,
            ),
        ],
    )

    engine = ArchiveEngine()

    assert engine.analyze(archive) == (
        ExtractDecision.EXTRACT_HERE
    )
