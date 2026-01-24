import sys
import ctypes
from PyQt6.QtWidgets import QMainWindow, QToolBar, QApplication, QDockWidget, QVBoxLayout, QDialog, QStatusBar
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt

from ui.pfd import PrimaryFlightDisplay
from ui.settings.altimeterSettingsPage import AltimeterSettingsPage
from ui.settings.artificialHorizonSettingsPage import ArtificialHorizonSettingsPage
from ui.ai import AIWidget

try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("AERIS")
except (AttributeError, OSError):
    pass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("AERIS")
        self.setWindowIcon(QIcon("software/assets/logo.png"))
        self.resize(1000, 700)

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
            QDockWidget {
                color: white;
            }
        """)

        self.pfdPage = PrimaryFlightDisplay()
        self.pfdPage.setStyleSheet("background-color: #000000;")
        self.setCentralWidget(self.pfdPage)

        self.SetupAIDock()

        self.SetupMenu()

    def SetupAIDock(self):
        self.aiPage = QDockWidget("Assistant IA", self)
        self.aiPage.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea | Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.TopDockWidgetArea | Qt.DockWidgetArea.BottomDockWidgetArea)
        
        self.aiWidget = AIWidget()
        self.aiWidget.setStyleSheet("background-color: #1E1E1E; color: white; border-left: 1px solid #333333;")
        
        self.aiPage.setWidget(self.aiWidget)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.aiPage)
        self.aiPage.hide()

    def SetupMenu(self):
        toolbar = QToolBar("My main toolbar")
        self.addToolBar(toolbar)
        toolbar.hide()

        self.aiAction = QAction("Assistant IA", self)
        self.aiAction.setCheckable(True)
        self.aiAction.triggered.connect(self.ToggleAI)
        toolbar.addAction(self.aiAction)

        toolbar.addSeparator()

        self.artificialHorizonAction = QAction("Horizon artificiel", self)
        self.artificialHorizonAction.triggered.connect(self.ShowArtificialHorizonSettingsPage)
        toolbar.addAction(self.artificialHorizonAction)

        toolbar.addSeparator()

        self.altimeterAction = QAction("Altimètre", self)
        self.altimeterAction.triggered.connect(self.ShowAltimeterSettingsPage)
        toolbar.addAction(self.altimeterAction)

        self.setStatusBar(QStatusBar(self))

        menu = self.menuBar()
        menu.addAction(self.aiAction)
        menu.addSeparator()
        settingsMenu = menu.addMenu("Paramètres")
        settingsMenu.addAction(self.artificialHorizonAction)
        settingsMenu.addAction(self.altimeterAction)

    def ToggleAI(self):
        isVisible = self.aiPage.isVisible()
        self.aiPage.setVisible(not isVisible)
        self.aiAction.setChecked(not isVisible)

    def ShowAltimeterSettingsPage(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Configuration de l'altimètre")
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout(dialog)

        settingsPage = AltimeterSettingsPage(self.pfdPage.altimeter)
        layout.addWidget(settingsPage)
        
        dialog.exec()

    def ShowArtificialHorizonSettingsPage(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Configuration de l'horizon artificiel")
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout(dialog)

        settingsPage = ArtificialHorizonSettingsPage(self.pfdPage.artificialHorizon)
        layout.addWidget(settingsPage)
        
        dialog.exec()

app = QApplication(sys.argv)
    
app.setStyle("Fusion") 
    
window = MainWindow()
window.show()

app.exec()