import sys
import ctypes
from PyQt6.QtWidgets import (
    QMainWindow, QToolBar, QApplication,
    QDockWidget, QVBoxLayout, QDialog, QStatusBar, QLabel
)
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt

from ui.pfd import PrimaryFlightDisplay
from ui.settings.altimeterSettingsPage import AltimeterSettingsPage
from ui.settings.artificialHorizonSettingsPage import ArtificialHorizonSettingsPage
from ui.settings.arduinoSettingsPage import ArduinoSettingsPage
from ui.ai import AIWidget


try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("AERIS")
except (AttributeError, OSError):
    pass


class MainWindow(QMainWindow):
    windowTitle = "AERIS"
    windowIcon = "software/assets/logo.png"

    def __init__(self):
        super().__init__()

        self.SetupWindow()
        self.SetupStyle()
        self.SetupCentralWidget()
        self.SetupAiDock()
        self.SetupMenu()



    def SetupWindow(self):
        self.setWindowTitle(self.windowTitle)
        self.setWindowIcon(QIcon(self.windowIcon))

    def SetupStyle(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #000000; }
            QToolBar {
                background-color: #121212;
                border-bottom: 1px solid #333333;
                spacing: 10px;
                padding: 5px;
            }
            QToolBar QWidget { color: white; }
            QStatusBar {
                background-color: #121212;
                border-top: 1px solid #333333;
                color: #888888;
            }
            QDockWidget { color: white; }
        """)

    def SetupCentralWidget(self):
        self.pfdPage = PrimaryFlightDisplay()
        self.setCentralWidget(self.pfdPage)

    def SetupAiDock(self):
        self.aiDock = QDockWidget("Assistant IA", self)
        self.aiDock.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)

        self.aiWidget = AIWidget()
        self.aiWidget.setStyleSheet(
            "background-color: #1E1E1E; color: white; border-left: 1px solid #333333;"
        )

        self.aiDock.setWidget(self.aiWidget)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.aiDock)
        self.aiDock.hide()

    def SetupMenu(self):
        toolbar = QToolBar("Main toolbar")
        self.addToolBar(toolbar)
        toolbar.hide()

        self.aiAction = QAction("Assistant IA", self, checkable=True)
        self.aiAction.triggered.connect(self.ToggleAi)

        self.artificialHorizonAction = QAction("Horizon artificiel", self)
        self.artificialHorizonAction.triggered.connect(
            lambda: self.OpenSettingsDialog(
                "Configuration de l'horizon artificiel",
                ArtificialHorizonSettingsPage,
                self.pfdPage.artificialHorizon
            )
        )

        self.altimeterAction = QAction("Altimètre", self)
        self.altimeterAction.triggered.connect(
            lambda: self.OpenSettingsDialog(
                "Configuration de l'altimètre",
                AltimeterSettingsPage,
                self.pfdPage.altimeter
            )
        )
        
        self.arduinoAction = QAction("Connexion", self)
        self.arduinoAction.triggered.connect(
            lambda: self.OpenSettingsDialog(
                "Connexion appareils",
                ArduinoSettingsPage,
                self
            )
        )

        toolbar.addActions([
            self.aiAction,
            self.artificialHorizonAction,
            self.altimeterAction,
            self.arduinoAction
        ])

        self.setStatusBar(QStatusBar(self))
        self.arduinoStatus = QLabel("🔴 Déconnecté")
        self.statusBar().addPermanentWidget(self.arduinoStatus)

        menu = self.menuBar()
        menu.addAction(self.aiAction)
        menu.addAction(self.arduinoAction)

        settingsMenu = menu.addMenu("Paramètres")
        settingsMenu.addActions([
            self.artificialHorizonAction,
            self.altimeterAction
        ])

    

    def ToggleAi(self, checked: bool):
        self.aiDock.setVisible(checked)

    def OpenSettingsDialog(self, title, pageClass, target):
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setMinimumWidth(400)

        layout = QVBoxLayout(dialog)
        layout.addWidget(pageClass(target))

        dialog.exec()

    def updateArduinoStatus(self, connected: bool):
        if connected:
            self.arduinoStatus.setText("🟢 Connecté")
        else:
            self.arduinoStatus.setText("🔴 Déconnecté")


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = MainWindow()
    window.showMaximized()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()