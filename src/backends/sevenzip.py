from __future__ import annotations

import shutil
from pathlib import Path
import subprocess

from .base import ArchiveBackend


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

    def list(self, archive: Path):
        raise NotImplementedError

    def extract(
        self,
        archive: Path,
        destination: Path,
    ) -> None:
        raise NotImplementedError

    def test(self, archive: Path) -> bool:
        raise NotImplementedError