#!/usr/bin/env bash

set -e

EXTENSION_FILE="$HOME/.local/share/nemo-python/extensions/nemo_smart_archive.py"

echo "Uninstalling NemoSmartArchive..."

if [ -f "$EXTENSION_FILE" ]; then
    rm "$EXTENSION_FILE"
    echo "Removed Nemo extension:"
    echo "  $EXTENSION_FILE"
else
    echo "NemoSmartArchive extension is not installed."
fi

echo "Restarting Nemo..."

nemo -q 2>/dev/null || true

echo
echo "NemoSmartArchive uninstalled successfully."