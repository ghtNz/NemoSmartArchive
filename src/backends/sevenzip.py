from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from src.models.archive import ArchiveEntry, ArchiveInfo
from src.models.errors import (
    ArchiveReadError,
    BackendUnavailableError,
    ExtractionError,
    PasswordRequiredError,
    UnsupportedArchiveError,
)

from .base import ArchiveBackend


class SevenZipBackend(ArchiveBackend):
    """7-Zip backend."""

    SUPPORTED_EXTENSIONS = (
        ".zip",
        ".7z",
        ".tar",
        ".tar.gz",
        ".tgz",
        ".tar.bz2",
        ".tar.xz",
    )

    @classmethod
    def is_supported(cls, archive: Path) -> bool:
        """Return True when the filename uses a supported archive format."""

        return archive.name.lower().endswith(cls.SUPPORTED_EXTENSIONS)

    def __init__(self) -> None:
        self._binary = shutil.which("7zz") or shutil.which("7z")

    @property
    def binary(self) -> str:
        if self._binary is None:
            raise BackendUnavailableError("7-Zip executable not found.")

        return self._binary

    def is_available(self) -> bool:
        return self._binary is not None

    def version(self) -> str:
        """Return installed 7-Zip version."""

        result = subprocess.run(
            [
                self.binary,
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        return result.stdout.strip()

    def list(self, archive: Path) -> ArchiveInfo:
        """List archive contents."""

        if not self.is_supported(archive):
            raise UnsupportedArchiveError(f"Unsupported archive format: {archive.name}")

        if not archive.is_file():
            raise ArchiveReadError(f"Archive not found: {archive}")

        try:
            result = subprocess.run(
                [
                    self.binary,
                    "l",
                    "-slt",
                    str(archive),
                ],
                capture_output=True,
                text=True,
                check=True,
            )

        except subprocess.CalledProcessError as error:
            output = error.stderr.strip() or error.stdout.strip()

            message = "Unable to read archive."

            lines = output.splitlines()

            for index, line in enumerate(lines):
                line = line.strip()

                if line == "ERRORS:":
                    for next_line in lines[index + 1 :]:
                        next_line = next_line.strip()

                        if next_line:
                            message = next_line
                            break

                    break

            raise ArchiveReadError(message) from error

        entries = self._parse_listing(result.stdout)

        return ArchiveInfo(
            path=archive,
            entries=entries,
        )

    def _parse_listing(
        self,
        output: str,
    ) -> list[ArchiveEntry]:
        """Parse 7-Zip technical listing."""

        entries: list[ArchiveEntry] = []

        current_path: str | None = None
        is_folder = False

        for line in output.splitlines():
            if line.startswith("Path = "):
                current_path = line.removeprefix("Path = ")

            elif line.startswith("Folder = "):
                is_folder = line.removeprefix("Folder = ") == "+"

                if current_path:
                    entries.append(
                        ArchiveEntry(
                            name=current_path,
                            is_directory=is_folder,
                        )
                    )

                    current_path = None

        return entries

    def extract(
        self,
        archive: Path,
        destination: Path,
    ) -> None:
        """Extract archive to destination."""

        if not self.is_supported(archive):
            raise UnsupportedArchiveError(f"Unsupported archive format: {archive.name}")

        if not archive.is_file():
            raise ArchiveReadError(f"Archive not found: {archive}")

        destination.mkdir(
            parents=True,
            exist_ok=True,
        )

        try:
            subprocess.run(
                [
                    self.binary,
                    "x",
                    str(archive),
                    f"-o{destination}",
                    "-y",
                ],
                capture_output=True,
                text=True,
                check=True,
            )

        except subprocess.CalledProcessError as error:
            message = (error.stdout + error.stderr).lower()

            if "password" in message or "encrypted" in message:
                from src.models.errors import (
                    PasswordRequiredError,
                )

                raise PasswordRequiredError("Archive password required") from error

            raise ExtractionError(
                error.stderr.strip() or "Unknown extraction error"
            ) from error

    def test(self, archive: Path) -> bool:
        """Test archive integrity using 7-Zip."""

        if not self.is_supported(archive):
            raise UnsupportedArchiveError(f"Unsupported archive format: {archive.name}")

        if not archive.is_file():
            raise ArchiveReadError(f"Archive not found: {archive}")

        result = subprocess.run(
            [
                self.binary,
                "t",
                "-p",
                str(archive),
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode == 0:
            return True

        message = (result.stderr.strip() or result.stdout.strip()).lower()

        if "password" in message or "encrypted" in message:
            raise PasswordRequiredError("Archive password required")

        return False
