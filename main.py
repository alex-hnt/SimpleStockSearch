# main.py (replace your MainFrame class with this)
import sys
import webbrowser
import keyboard

from PySide6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QHBoxLayout
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, Signal, QPointF

from TrayIcon import TrayIcon
from SettingsMenu import SettingsMenu
import settings as usersettings
import themes


class MainFrame(QWidget):
    # Qt signal used to ask the GUI thread to show the popup
    show_popup_signal = Signal()

    def __init__(self, settings):
        super().__init__(parent=None)
        self.settings = settings
        self.hotkey_handle = None 
        self._drag_pos = None

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint) 

        self.setStyleSheet(
            f"background-color: {themes.default_dark['BACKGROUND']};"
            f"font-family: {themes.default_dark['FONT']};"
            f"font-size: 50pt;"
        )

        self.resize(300, 125)
        screen = QApplication.primaryScreen().geometry()
        self.move((screen.width() - 300) // 2, (screen.height() - 150) // 2)

        self.tray_icon = TrayIcon(self)

        self.label = QLabel("$")
        self.label.setStyleSheet(f"color: {themes.default_dark['TEXT']};")

        self.text_field = QLineEdit()
        self.text_field.setMaxLength(4)
        self.text_field.setStyleSheet(
            f"background-color: {themes.default_dark['BACKGROUND']}; "
            f"color: {themes.default_dark['TEXT_INPUT']}; border: none;"
        )
        self.text_field.setFocus()

        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.text_field)
        layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(layout)

        self.label.mousePressEvent = self.on_label_clicked
        self.text_field.textEdited.connect(self.on_char_typed)
        self.text_field.returnPressed.connect(self.on_text_field_submit)

        self.show_popup_signal.connect(self.show_popup)

        # Register hotkey (this installs keyboard callback that emits the signal)
        self.register_hotkey(self.settings["hotkey"])

    def on_label_clicked(self, event):
        if event.button() == Qt.LeftButton:
            dlg = SettingsMenu(self, self.settings, self.reassign_hotkey)
            dlg.show()

    def on_char_typed(self, text):
        cursor = self.text_field.cursorPosition()
        up = text.upper()
        if up != text:
            self.text_field.blockSignals(True)
            self.text_field.setText(up)
            self.text_field.setCursorPosition(cursor)
            self.text_field.blockSignals(False)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self._drag_pos is not None:
            self.move((event.globalPosition() - self._drag_pos).toPoint())
            event.accept()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.hide()
        else:
            super().keyPressEvent(event)

    def on_text_field_submit(self):
        symbol = self.text_field.text().strip()
        if not symbol:
            return

        for key in self.settings["enabled_sites_keys"]:
            url = usersettings.SITES.get(key).format(symbol=symbol)
            if url:
                webbrowser.open_new_tab(url)

        self.hide()

    def show_popup(self):
        self.show()
        self.raise_()
        self.activateWindow()
        self.text_field.setFocus()

    def register_hotkey(self, hotkey):
        if self.hotkey_handle is not None:
            try:
                keyboard.remove_hotkey(self.hotkey_handle)
            except Exception:
                pass

        def _emit_show():
            try:
                self.show_popup_signal.emit()
            except Exception:
                pass

        self.hotkey_handle = keyboard.add_hotkey(hotkey, _emit_show)

    def reassign_hotkey(self):
        self.register_hotkey(self.settings["hotkey"])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    settings = usersettings.load_settings(usersettings.SETTINGS_FILE, usersettings.DEFAULT_SETTINGS)
    popup = MainFrame(settings=settings)
    popup.show()
    sys.exit(app.exec())
