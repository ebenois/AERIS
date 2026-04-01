from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSpinBox
from PyQt6.QtCore import QSettings
from services.ESP32Client import ESP32Client


class DeviceSettingsPage(QWidget):
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.pfd = mainWindow.pfdPage
        self.settings = QSettings("ENSC", "AERIS")

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Port d'écoute UDP (ex: 1234) :"))

        self.portSpin = QSpinBox()
        self.portSpin.setRange(1, 65535)
        self.portSpin.setValue(int(self.settings.value("UdpPort", 1234)))
        layout.addWidget(self.portSpin)

        self.connectButton = QPushButton("Établir la connexion")
        self.connectButton.clicked.connect(self.applySettings)
        layout.addWidget(self.connectButton)

        self.statusLabel = QLabel()
        layout.addWidget(self.statusLabel)
        self.updateUI()

    def applySettings(self):
        newPort = self.portSpin.value()
        self.settings.setValue("UdpPort", newPort)

        # Fermeture propre de l'ancien socket
        if self.pfd.device:
            self.pfd.device.close()

        try:
            newClient = ESP32Client(port=newPort)
            self.pfd.setDevice(newClient)
            self.statusLabel.setText("✅ Port configuré avec succès")
        except Exception as e:
            self.statusLabel.setText(f"❌ Erreur: {e}")

    def updateUI(self):
        if self.pfd.isConnected:
            self.statusLabel.setText("🟢 Réception de données en cours")
        else:
            self.statusLabel.setText("🔴 Déconnecté (en attente de paquets)")
