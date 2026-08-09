"""
Desktop notification helpers.
"""

from __future__ import annotations

import subprocess


def notify(
    title: str,
    message: str,
) -> None:
    """
    Send desktop notification.
    """

    try:
        subprocess.run(
            [
                "notify-send",
                title,
                message,
            ],
            check=False,
        )

    except Exception:
        # Notification failure should
        # never break extraction.
        pass
