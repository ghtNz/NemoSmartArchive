"""
UnRAR archive backend.
"""

from __future__ import annotations

import re
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


class UnrarBackend(ArchiveBackend):
    """RAR archive backend using UnRAR."""

    SUPPORTED_EXTENSIONS = (".rar",)

    def __init__(self) -> None:
        self._binary = shutil.which("unrar")

    @classmethod
    def is_supported(cls, archive: Path) -> bool:
        """Return True when the filename is a RAR archive."""
        return archive.name.lower().endswith(cls.SUPPORTED_EXTENSIONS)

    @property
    def binary(self) -> str:
        if self._binary is None:
            raise BackendUnavailableError("UnRAR executable not found.")

        return self._binary

    def is_available(self) -> bool:
        return self._binary is not None

    def version(self) -> str:
        """Return installed UnRAR version."""
        result = subprocess.run(
            [self.binary],
            capture_output=True,
            text=True,
            check=False,
        )

        output = result.stdout or result.stderr
        match = re.search(r"UNRAR\s+[\d.]+", output, re.IGNORECASE)

        return match.group(0) if match else output.strip()

    def list(self, archive: Path) -> ArchiveInfo:
        """List archive contents using technical listing."""

        self._validate_archive(archive)

        try:
            result = subprocess.run(
                [self.binary, "lt", str(archive)],
                capture_output=True,
                text=True,
                check=True,
            )

        except subprocess.CalledProcessError as error:
            self._raise_command_error(error, "Unable to read archive.")

        entries = self._parse_listing(result.stdout)

        return ArchiveInfo(
            path=archive,
            entries=entries,
        )

    def _parse_listing(self, output: str) -> list[ArchiveEntry]:
        """Parse UnRAR technical listing."""

        entries: list[ArchiveEntry] = []

        for block in re.split(r"\n\s*\n", output):
            name_match = re.search(r"^\s*Name:\s*(.+?)\s*$", block, re.MULTILINE)
            type_match = re.search(
                r"^\s*Type:\s*(File|Directory)\s*$", block, re.MULTILINE
            )

            if not name_match or not type_match:
                continue

            name = name_match.group(1)

            if not name:
                continue

            entries.append(
                ArchiveEntry(
                    name=name,
                    is_directory=type_match.group(1) == "Directory",
                )
            )

        if not entries:
            raise ArchiveReadError("No archive entries found.")

        return entries

    def extract(
        self,
        archive: Path,
        destination: Path,
    ) -> None:
        """Extract RAR archive while preserving directory structure."""

        self._validate_archive(archive)

        destination.mkdir(
            parents=True,
            exist_ok=True,
        )

        try:
            subprocess.run(
                [
                    self.binary,
                    "x",
                    "-y",
                    str(archive),
                    str(destination) + "/",
                ],
                capture_output=True,
                text=True,
                check=True,
            )

        except subprocess.CalledProcessError as error:
            self._raise_command_error(error, "Unable to extract archive.")

    def test(self, archive: Path) -> bool:
        """Test RAR archive integrity."""

        self._validate_archive(archive)

        try:
            result = subprocess.run(
                [
                    self.binary,
                    "t",
                    "-p-",
                    str(archive),
                ],
                capture_output=True,
                text=True,
                check=False,
            )

        except OSError as error:
            raise ExtractionError(str(error)) from error

        if result.returncode == 0:
            return True

        message = (result.stdout + result.stderr).lower()

        if "password" in message or "encrypted" in message:
            raise PasswordRequiredError("Archive password required")

        return False

    def _validate_archive(self, archive: Path) -> None:
        """Validate archive format and existence."""

        if not self.is_supported(archive):
            raise UnsupportedArchiveError(f"Unsupported archive format: {archive.name}")

        if not archive.is_file():
            raise ArchiveReadError(f"Archive not found: {archive}")

        _ = self.binary

    @staticmethod
    def _raise_command_error(
        error: subprocess.CalledProcessError,
        default_message: str,
    ) -> None:
        """Translate UnRAR command failures into application errors."""

        output = (error.stdout or "") + (error.stderr or "")
        message = output.lower()

        if "password" in message or "encrypted" in message:
            raise PasswordRequiredError("Archive password required") from error

        raise ArchiveReadError(output.strip() or default_message) from error
