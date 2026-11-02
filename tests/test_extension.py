from pathlib import Path

from src.extension import (
    extract_many_smart,
    extract_smart,
    is_supported_archive,
)
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


def test_supported_archive_formats():
    supported = (
        "archive.zip",
        "archive.7z",
        "archive.tar",
        "archive.rar",
        "archive.RAR",
    )

    for filename in supported:
        assert is_supported_archive(Path(filename))


def test_unsupported_archive_formats():
    unsupported = (
        "photo.jpg",
        "document.pdf",
        "video.mp4",
    )

    for filename in unsupported:
        assert not is_supported_archive(Path(filename))


def test_extract_many_smart_success(tmp_path, monkeypatch):
    from src import extension

    notifications = []

    monkeypatch.setattr(
        extension,
        "notify",
        lambda title, message: notifications.append((title, message)),
    )

    archives = [
        Path("tests/data/loose_files.zip"),
        Path("tests/data/loose_files.zip"),
    ]

    results = extract_many_smart(archives, tmp_path)

    assert len(results) == 2
    assert all(result.status == ExtractionStatus.SUCCESS for result in results)

    assert len(notifications) == 1

    assert "2 archives processed" in notifications[0][1]
    assert "2 successful" in notifications[0][1]
    assert "0 failed" in notifications[0][1]


def test_extract_many_smart_with_failure(tmp_path, monkeypatch):
    from src import extension

    notifications = []

    monkeypatch.setattr(
        extension,
        "notify",
        lambda title, message: notifications.append((title, message)),
    )

    archives = [
        Path("tests/data/loose_files.zip"),
        Path("tests/data/corrupt.zip"),
    ]

    results = extract_many_smart(archives, tmp_path)

    assert results[0].status == ExtractionStatus.SUCCESS
    assert results[1].status == ExtractionStatus.FAILED

    assert len(notifications) == 1

    summary = notifications[0][1]

    assert "2 archives processed" in summary
    assert "1 successful" in summary
    assert "1 failed" in summary
    assert "corrupt.zip" in summary


def test_extract_many_smart_suppresses_individual_notifications(
    tmp_path,
    monkeypatch,
):
    from src import extension

    notifications = []

    monkeypatch.setattr(
        extension,
        "notify",
        lambda title, message: notifications.append((title, message)),
    )

    extract_many_smart(
        [
            Path("tests/data/loose_files.zip"),
            Path("tests/data/loose_files.zip"),
        ],
        tmp_path,
    )

    assert len(notifications) == 1
    assert "archives processed" in notifications[0][1]
