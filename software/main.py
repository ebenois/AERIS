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

        self.setupAIDock()

        self.setupToolbar()

    def setupAIDock(self):
        self.aiPage = QDockWidget("Assistant IA", self)
        self.aiPage.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea | Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.TopDockWidgetArea | Qt.DockWidgetArea.BottomDockWidgetArea)
        
        self.aiWidget = AIWidget()
        self.aiWidget.setStyleSheet("background-color: #1E1E1E; color: white; border-left: 1px solid #333333;")
        
        self.aiPage.setWidget(self.aiWidget)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.aiPage)
        self.aiPage.hide()

    def setupToolbar(self):
        toolbar = self.addToolBar("Navigation")
        toolbar.setMovable(False)

        self.aiAction = QAction("Assistant IA", self)
        self.aiAction.setCheckable(True)
        self.aiAction.triggered.connect(self.toggleAI)
        toolbar.addAction(self.aiAction)

        toolbar.addSeparator()

        settingsAction = QAction("Paramètres", self)
        settingsAction.triggered.connect(self.showSettings)
        toolbar.addAction(settingsAction)

    def toggleAI(self):
        is_visible = self.aiPage.isVisible()
        self.aiPage.setVisible(not is_visible)
        self.aiAction.setChecked(not is_visible)

    def showSettings(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Configuration AERIS")
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(SettingsPage())
        
        dialog.exec()

app = QApplication(sys.argv)
    
app.setStyle("Fusion") 
    
window = MainWindow()
window.show()

app.exec()