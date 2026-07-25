from __future__ import annotations

import shutil
from pathlib import Path
import subprocess

from .base import ArchiveBackend
from src.models.archive import ArchiveEntry, ArchiveInfo


class SevenZipBackend(ArchiveBackend):
    """7-Zip backend."""

    def __init__(self) -> None:
        self._binary = shutil.which("7zz") or shutil.which("7z")

    @property
    def binary(self) -> str:
        if self._binary is None:
            raise RuntimeError("7-Zip executable not found.")

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

                is_folder = (
                    line.removeprefix("Folder = ")
                    == "+"
                )

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
        raise NotImplementedError

    def test(self, archive: Path) -> bool:
        raise NotImplementedError