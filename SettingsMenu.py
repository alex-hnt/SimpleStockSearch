from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QCheckBox, QWidget, QGridLayout, QComboBox
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
import keyboard
import settings as usersettings
from themes import Theme

class Checkboxes(QWidget):
    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.settings = settings
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.boxes = []
        for key in usersettings.SITES:
            cb = QCheckBox(key)
            cb.setChecked(key in settings["enabled_sites_keys"])
            self.boxes.append(cb)
            layout.addWidget(cb)

        layout.addStretch()
        self.setLayout(layout)

    def get_checked_indices(self):
        return [i for i, cb in enumerate(self.boxes) if cb.isChecked()]


class SettingsMenu(QDialog):
    def __init__(self, parent, settings, reassign_hotkey_callback, repaint_theme_callback):
        super().__init__(parent)
        self.frame = parent
        self.settings = settings
        self.reassign_hotkey_callback = reassign_hotkey_callback
        self.repaint_theme_callback = repaint_theme_callback

        self.setWindowTitle("Settings")
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.initStylesheet()
        self.resize(400, 250)

        main_layout = QVBoxLayout(self)
        row_layout = QHBoxLayout()
        button_layout = QHBoxLayout()
        hotkey_layout = QVBoxLayout()

        self.checkboxes = Checkboxes(settings, self)
        row_layout.addWidget(self.checkboxes, 2)

        self.hotkey_label = QLabel(self.settings["hotkey"])

        self.hotkey_button = QPushButton("Change Hotkey")
        self.hotkey_button.clicked.connect(self.on_hotkey_button)

        self.theme_dropdown = QComboBox()
        for theme in Theme:
            self.theme_dropdown.addItem(theme)
        self.theme_dropdown.setCurrentIndex(self.theme_dropdown.findText(self.settings['theme']))
        self.theme_dropdown.currentTextChanged.connect(self.on_theme_selected)

        hotkey_layout.addWidget(self.hotkey_label)
        hotkey_layout.addWidget(self.hotkey_button)
        hotkey_layout.addStretch()
        hotkey_layout.addWidget(self.theme_dropdown)
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

    def initStylesheet(self):
        self.setStyleSheet(
            f"background-color: {Theme[self.settings['theme']]['BACKGROUND']};" 
            f"color: {Theme[self.settings['theme']]['TEXT']};"
            f"font-family: {Theme[self.settings['theme']]['FONT']};"
            f"font-size: 12pt;"
        )
    
    def on_theme_selected(self, theme):
        self.settings["theme"] = theme
        self.repaint_theme_callback()
        self.initStylesheet()
        self.update()
        print(self.settings)

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
