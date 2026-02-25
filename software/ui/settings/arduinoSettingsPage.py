from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox
from PyQt6.QtCore import QSettings
from services.arduino import ArduinoReader


class ArduinoSettingsPage(QWidget):
    def __init__(self, mainWindow):
        super().__init__()

        self.mainWindow = mainWindow
        self.pfd = mainWindow.pfdPage
        self.settings = QSettings("ENSC", "AERIS")

        self.arduino = self.pfd.arduino or ArduinoReader()

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Port série détecté :"))

        self.portBox = QComboBox()
        layout.addWidget(self.portBox)

        self.refreshButton = QPushButton("Rafraîchir les ports")
        layout.addWidget(self.refreshButton)

        self.connectButton = QPushButton()
        layout.addWidget(self.connectButton)

        self.statusLabel = QLabel()
        layout.addWidget(self.statusLabel)

        self.refreshButton.clicked.connect(self.loadPorts)
        self.connectButton.clicked.connect(self.toggleConnection)

        self.loadPorts()
        self.restoreLastPort()
        self.updateUI()

    def loadPorts(self):
        self.portBox.clear()
        ports = ArduinoReader.available_ports()
        self.portBox.addItems(ports)

    def restoreLastPort(self):
        lastPort = self.settings.value("Port", "")
        index = self.portBox.findText(lastPort)
        if index >= 0:
            self.portBox.setCurrentIndex(index)

    def toggleConnection(self):
        if self.arduino.is_connected():
            self.arduino.disconnect()
            self.pfd.setArduino(None)
            self.mainWindow.updateArduinoStatus(False)
        else:
            port = self.portBox.currentText()
            if self.arduino.connect(port):
                self.settings.setValue("ArduinoPort", port)
                self.pfd.setArduino(self.arduino)
                self.mainWindow.updateArduinoStatus(True)

        self.updateUI()

    def updateUI(self):
        if self.arduino.is_connected():
            self.statusLabel.setText("🟢 Connecté")
            self.connectButton.setText("Déconnecter")
        else:
            self.statusLabel.setText("🔴 Déconnecté")
            self.connectButton.setText("Connecter")
