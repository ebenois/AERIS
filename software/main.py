import sys
import ctypes
from PyQt6.QtWidgets import QMainWindow, QToolBar, QApplication, QDockWidget, QVBoxLayout, QDialog
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt

from ui.pfd import PrimaryFlightDisplay
from ui.settings import SettingsPage
from ui.ai import AIWidget

try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("AERIS")
except AttributeError:
    pass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AERIS")
        self.setWindowIcon(QIcon("software/assets/logo.png"))

        self.pfdPage = PrimaryFlightDisplay()
        self.setCentralWidget(self.pfdPage)

        toolbar = QToolBar("Navigation")
        self.addToolBar(toolbar)

        self.aiPage = QDockWidget("AI", self)
        self.aiWidget = AIWidget()
        self.aiPage.setWidget(self.aiWidget)
        self.aiPage.setFloating(False)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.aiPage)
        self.aiPage.hide()

        self.aiButton = QAction("AI", self)
        self.aiButton.triggered.connect(self.toggleAi)
        toolbar.addAction(self.aiButton)

        self.settingsButton = QAction("Settings", self)
        self.settingsButton.triggered.connect(self.showSettings)
        toolbar.addAction(self.settingsButton)

    def toggleAi(self):
        if self.aiPage.isVisible():
            self.aiPage.hide()
        else:
            self.aiPage.show()

    def showSettings(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Settings")
        layout = QVBoxLayout()
        layout.addWidget(SettingsPage())
        dialog.setLayout(layout)
        dialog.exec()

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()