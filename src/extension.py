from gi.repository import GObject, Nemo, Gtk


class SmartArchiveExtension(GObject.GObject, Nemo.MenuProvider):
    def get_file_items(self, files):
        if len(files) != 1:
            return

        file = files[0]

        if file.is_directory():
            return

        uri = file.get_uri().lower()

        supported = (
            ".zip",
            ".7z",
            ".rar",
            ".tar",
            ".gz",
            ".bz2",
            ".xz",
        )

        if not uri.endswith(supported):
            return

        item = Nemo.MenuItem(
            name="NemoSmartArchive::ExtractSmart",
            label="⭐ Extract Here (Smart)",
            tip="Extract archive intelligently",
        )

        item.connect("activate", self.menu_activate_cb, file)

        return [item]

    def menu_activate_cb(self, menu, file):
        dialog = Gtk.MessageDialog(
            text="Nemo Smart Archive",
            secondary_text="The extension is working!",
            buttons=Gtk.ButtonsType.OK,
        )

        dialog.run()
        dialog.destroy()