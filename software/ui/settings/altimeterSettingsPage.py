import sys
from PyQt6.QtWidgets import (
    QWidget, 
    QLabel, 
    QVBoxLayout, 
    QHBoxLayout, 
    QSlider, 
    QPushButton,
    QGroupBox
)
from PyQt6.QtCore import Qt, QSettings, pyqtSignal

from ui.settings.settingGroup import SettingGroup

class AltimeterSettingsPage(QWidget):
    def __init__(self, instrument):
        super().__init__()
        self.settings = QSettings("ENSC", "AERIS")
        self.instrument = instrument

        mainLayout = QVBoxLayout(self)

        altimeterGroup, altimeterLayout = self.createSection("Altimètre")
        indicatorGroup, indicatorLayout = self.createSection("Indicateur")
        backgroundGroup, backgroundLayout = self.createSection("Fond")
        graduationsGroup, graduationsLayout = self.createSection("Graduations")

        mainLayout.addWidget(indicatorGroup)
        mainLayout.addWidget(backgroundGroup)
        mainLayout.addWidget(graduationsGroup)

    def saveAndUpdate(self, key, value, callbackFunc):
        self.settings.setValue(key, value)
        self.settings.sync()
        callbackFunc(value)

    def createSection(self, title):
        group = QGroupBox(title)
        layout = QVBoxLayout(group)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        return group, layout