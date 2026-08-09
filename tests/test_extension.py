from pathlib import Path

from src.extension import extract_smart
from src.models.archive import ExtractionStatus


def test_extract_smart_loose_files(tmp_path):
    archive = Path("tests/data/loose_files.zip")

    result = extract_smart(
        archive,
        tmp_path,
    )

    expected = tmp_path / "loose_files"

    assert result.status == (ExtractionStatus.SUCCESS)

    assert result.output == expected

    assert expected.is_dir()

    assert (expected / "file1.txt").is_file()

    assert (expected / "file2.txt").is_file()


def test_extract_smart_corrupt_archive(tmp_path):
    archive = Path("tests/data/corrupt.zip")

    result = extract_smart(
        archive,
        tmp_path,
    )

    assert result.status == (ExtractionStatus.FAILED)

    assert result.error == ("Unexpected end of archive")


def test_extract_smart_password_archive(tmp_path):
    archive = Path("tests/data/password.zip")

    result = extract_smart(
        archive,
        tmp_path,
    )

    assert result.status == (ExtractionStatus.FAILED)

    assert result.error == ("Archive password required")


def test_extract_smart_unsupported_archive(tmp_path):
    archive = Path("tests/data/photo.jpg")

    result = extract_smart(
        archive,
        tmp_path,
    )

    assert result.status == (ExtractionStatus.FAILED)

    assert result.error == ("Unsupported archive format: photo.jpg")


def test_extract_smart_missing_archive(tmp_path):
    archive = Path("tests/data/missing.zip")

    result = extract_smart(
        archive,
        tmp_path,
    )

    assert result.status == (ExtractionStatus.FAILED)

    assert result.error == ("Archive not found: tests/data/missing.zip")
