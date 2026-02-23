from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
    QLabel
)
from services.arduino import ArduinoReader


class ArduinoSettingsPage(QWidget):
    def __init__(self, pfd):
        super().__init__()

        self.pfd = pfd
        self.arduino = pfd.arduino

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Port COM :"))

        self.portInput = QLineEdit("COM3")
        layout.addWidget(self.portInput)

        self.connectButton = QPushButton("Connecter")
        layout.addWidget(self.connectButton)

        self.statusLabel = QLabel("Déconnecté")
        layout.addWidget(self.statusLabel)

        self.connectButton.clicked.connect(self.toggleConnection)

        self.updateStatus()

    def toggleConnection(self):
        port = self.portInput.text()

        if self.arduino and self.arduino.is_connected():
            self.arduino.disconnect()
            self.pfd.setArduino(None)
            self.arduino = None

        else:
            self.arduino = ArduinoReader()
            success = self.arduino.connect(port)

            if success:
                self.pfd.setArduino(self.arduino)
            else:
                self.arduino = None

        self.updateStatus()

    def updateStatus(self):
        if self.arduino and self.arduino.is_connected():
            self.statusLabel.setText("Connecté")
            self.connectButton.setText("Déconnecter")
        else:
            self.statusLabel.setText("Déconnecté")
            self.connectButton.setText("Connecter")