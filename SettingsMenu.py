from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QCheckBox, QWidget, QGridLayout
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
import keyboard
import settings as usersettings
import themes


class Checkboxes(QWidget):
    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.settings = settings
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.boxes = []
        for key in usersettings.SITE_KEYS:
            cb = QCheckBox(key)
            cb.setChecked(key in settings["enabled_sites_keys"])
            self.boxes.append(cb)
            layout.addWidget(cb)

        layout.addStretch()
        self.setLayout(layout)

    def get_checked_indices(self):
        return [i for i, cb in enumerate(self.boxes) if cb.isChecked()]


class SettingsMenu(QDialog):
    def __init__(self, parent, settings, reassign_hotkey_callback):
        super().__init__(parent)
        self.frame = parent
        self.settings = settings
        self.reassign_hotkey_callback = reassign_hotkey_callback

        self.setWindowTitle("Settings")
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setStyleSheet(
            f"background-color: {themes.default_dark['BACKGROUND']};" 
            f"color: {themes.default_dark['TEXT']};"
            f"font-family: {themes.default_dark['FONT']};"
            f"font-size: 12pt;"
        )
        self.resize(400, 250)

        main_layout = QVBoxLayout(self)
        row_layout = QHBoxLayout()
        button_layout = QHBoxLayout()
        hotkey_layout = QVBoxLayout()

        self.checkboxes = Checkboxes(settings, self)
        row_layout.addWidget(self.checkboxes, 2)

        self.hotkey_label = QLabel(self.settings["hotkey"])
        self.hotkey_label.setFont(QFont(themes.default_dark['FONT'], 12))
        self.hotkey_label.setStyleSheet(f"color: {themes.default_dark['TEXT']};")

        self.hotkey_button = QPushButton("Change Hotkey")
        self.hotkey_button.clicked.connect(self.on_hotkey_button)

        hotkey_layout.addWidget(self.hotkey_label)
        hotkey_layout.addWidget(self.hotkey_button)
        hotkey_layout.addStretch()

        row_layout.addLayout(hotkey_layout, 1)

        self.save_button = QPushButton("Save")
        self.back_button = QPushButton("Back")

        self.save_button.clicked.connect(self.on_save)
        self.back_button.clicked.connect(self.on_exit)

        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.back_button)

        main_layout.addLayout(row_layout)
        main_layout.addLayout(button_layout)

    def on_hotkey_button(self):
        self.hotkey_label.setText("Recording hotkey...")
        self.repaint()
        hotkey = keyboard.read_hotkey(suppress=False)
        if hotkey != "esc":
            self.hotkey_label.setText(hotkey)
            self.settings["hotkey"] = hotkey
        else:
            self.hotkey_label.setText(self.settings["hotkey"])

    def on_save(self):
        checked_indices = self.checkboxes.get_checked_indices()
        usersettings.save_settings(
            usersettings.SETTINGS_FILE, self.settings, checked_indices
        )
        self.reassign_hotkey_callback()
        self.on_exit()

    def on_exit(self):
        self.close()
