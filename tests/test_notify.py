from src.ui.notify import notify


def test_notify_runs():

    # Should not raise exception
    notify(
        "NemoSmartArchive",
        "Test notification",
    )
