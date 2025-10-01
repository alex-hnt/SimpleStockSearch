from PySide6.QtWidgets import QSystemTrayIcon, QMenu 
from PySide6.QtGui import QIcon, QAction

class TrayIcon(QSystemTrayIcon):
    def __init__(self, frame):
        super().__init__()
        self.frame = frame

        self.setIcon(QIcon.fromTheme("dialog-information"))
        self.setToolTip("SimpleStockSearch")
        self.setVisible(True)

        menu = QMenu()
        show_action = QAction("Show", self)
        exit_action = QAction("Exit", self)

        show_action.triggered.connect(self.frame.show_popup)
        exit_action.triggered.connect(self.on_exit)

        menu.addAction(show_action)
        menu.addAction(exit_action)
        self.setContextMenu(menu)

        self.activated.connect(self.on_click)

    def on_click(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.frame.show_popup()

    def on_exit(self):
        self.frame.close()
        self.hide()
