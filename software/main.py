import sys
import ctypes
from PyQt6.QtWidgets import (
    QMainWindow,
    QToolBar,
    QApplication,
    QDockWidget,
    QVBoxLayout,
    QDialog,
    QStatusBar,
    QLabel,
)
from PyQt6.QtGui import QIcon, QAction, QFontDatabase, QFont
from PyQt6.QtCore import Qt

from ui.pfd import PrimaryFlightDisplay
from ui.settings.altimeterSettingsPage import AltimeterSettingsPage
from ui.settings.deviceSettingsPage import DeviceSettingsPage
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
            * {
                font-family: "B612 Mono";
            }
            QMainWindow { background-color: #000000; }
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

        self.altimeterAction = QAction("Altimètre", self)
        self.altimeterAction.triggered.connect(
            lambda: self.OpenSettingsDialog(
                "Configuration de l'altimètre",
                AltimeterSettingsPage,
                self.pfdPage.instruments[4],
            )
        )

        self.deviceAction = QAction("Connexion", self)
        self.deviceAction.triggered.connect(
            lambda: self.OpenSettingsDialog(
                "Connexion appareils", DeviceSettingsPage, self
            )
        )

        toolbar.addActions(
            [
                self.aiAction,
                self.altimeterAction,
                self.deviceAction,
            ]
        )

        self.setStatusBar(QStatusBar(self))
        self.deviceStatus = QLabel("🔴 Déconnecté ")
        self.statusBar().addPermanentWidget(self.deviceStatus)

        menu = self.menuBar()
        menu.addAction(self.aiAction)
        menu.addAction(self.deviceAction)

        settingsMenu = menu.addMenu("Paramètres")
        settingsMenu.addActions([self.altimeterAction])

    def ToggleAi(self, checked: bool):
        self.aiDock.setVisible(checked)

    def OpenSettingsDialog(self, title, pageClass, target):
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setMinimumWidth(400)

        layout = QVBoxLayout(dialog)
        layout.addWidget(pageClass(target))

        dialog.exec()

    def updateDeviceStatus(self, connected: bool):
        if connected:
            self.deviceStatus.setText("🟢 Connecté ")
        else:
            self.deviceStatus.setText("🔴 Déconnecté ")


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    font_id = QFontDatabase.addApplicationFont(
        "software/assets/B612_Mono/B612Mono-Regular.ttf"
    )

    if font_id != -1:
        family = QFontDatabase.applicationFontFamilies(font_id)[0]
        app.setFont(QFont(family))
        print(f"Police chargée : {family}")
    else:
        print("Erreur chargement police")

    window = MainWindow()
    window.showMaximized()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
