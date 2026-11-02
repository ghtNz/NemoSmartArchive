#!/usr/bin/env bash

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NEMO_EXTENSION_DIR="$HOME/.local/share/nemo-python/extensions"
EXTENSION_FILE="$NEMO_EXTENSION_DIR/nemo_smart_archive.py"

echo "Installing NemoSmartArchive..."
echo "Project directory: $PROJECT_DIR"

mkdir -p "$NEMO_EXTENSION_DIR"

cat > "$EXTENSION_FILE" <<EOF
"""
NemoSmartArchive Nemo extension.
"""

import sys
from pathlib import Path

import gi

gi.require_version("Nemo", "3.0")

from gi.repository import Nemo, GObject

sys.path.insert(
    0,
    "$PROJECT_DIR"
)

from src.extension import (
    extract_many_smart,
    extract_smart,
    is_supported_archive,
)


class NemoSmartArchiveExtension(
    GObject.GObject,
    Nemo.MenuProvider,
):

    def __init__(self):
        super().__init__()

    def get_file_items(
        self,
        window,
        files,
    ):

        if not files:
            return

        for file in files:
            if file.is_directory():
                return

            location = file.get_location()
            file_path = location.get_path()

            if not file_path:
                return

            if not is_supported_archive(Path(file_path)):
                return

        menu_item = Nemo.MenuItem(
            name="NemoSmartArchive::SmartExtract",
            label="Extract Here (Smart)",
            tip="Smart extract selected archive",
        )

        menu_item.connect(
            "activate",
            self.on_activate,
            files,
        )

        return [menu_item]

    def on_activate(
        self,
        menu_item,
        files,
    ):
        paths = []

        for file in files:
            location = file.get_location()
            file_path = location.get_path()

            if file_path:
                paths.append(Path(file_path))

        if not paths:
            return

        try:
            if len(paths) == 1:
                extract_smart(paths[0])
            else:
                extract_many_smart(paths)

        except Exception as error:
            print(
                "NemoSmartArchive error:",
                error,
            )
EOF

chmod 644 "$EXTENSION_FILE"

echo "Restarting Nemo..."

nemo -q 2>/dev/null || true

echo
echo "NemoSmartArchive installed successfully."
echo "Extension:"
echo "  $EXTENSION_FILE"