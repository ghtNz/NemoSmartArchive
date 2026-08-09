"""
Smart archive decision engine.
"""

from __future__ import annotations

from src.models.archive import (
    ArchiveEntry,
    ArchiveInfo,
    ExtractDecision,
)


class ArchiveEngine:
    """Analyze archive structure."""

    def analyze(
        self,
        archive: ArchiveInfo,
    ) -> ExtractDecision:
        """
        Decide extraction behavior.
        """

        top_level = self._top_level_items(archive)

        if len(top_level) == 1:
            item = top_level[0]

            if item.is_directory:
                return ExtractDecision.EXTRACT_HERE

        return ExtractDecision.CREATE_FOLDER

    def _top_level_items(
        self,
        archive: ArchiveInfo,
    ) -> list[ArchiveEntry]:
        """
        Return unique top-level entries.
        """

        result = {}

        for entry in archive.entries:
            parts = entry.name.split("/")

            if len(parts) == 1:
                name = parts[0]

                result[name] = entry

            else:
                name = parts[0]

                result[name] = ArchiveEntry(
                    name=name + "/",
                    is_directory=True,
                )

        return list(result.values())
