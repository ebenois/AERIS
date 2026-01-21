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

class SettingsPage(QWidget):
    def __init__(self, instrument):
        super().__init__()
        self.settings = QSettings("ENSC", "AERIS")
        self.instrument = instrument

        mainLayout = QVBoxLayout(self)
        planeGroup, planeLayout = self.createSection("Avion")

        lineWeight = self.settings.value("lineWeight", 10, int)
        dotSize = self.settings.value("dotSize", 10, int)
        outlineWeight = self.settings.value("outlineWeight", 5, int)
        wingsDistance = self.settings.value("wingsDistance", 45, int)
        wingsSpan = self.settings.value("wingsSpan", 75, int)
        wingsHeight = self.settings.value("wingsHeight", 12, int)

        self.lineWeightControl = SettingGroup("Line weight", 0, 30, lineWeight, 10)
        self.dotSizeControl = SettingGroup("Dot size", 0, 30, dotSize, 10)
        self.outlineWeightControl = SettingGroup("Outline weight", 0, 15, outlineWeight, 5)
        self.wingsDistanceControl = SettingGroup("Distance between wings", 1, 100, wingsDistance, 45)
        self.wingsSpanControl = SettingGroup("Wings span", 1, 100, wingsSpan, 75)
        self.wingsHeightControl = SettingGroup("Wings height", 1, 100, wingsHeight, 12)

        self.lineWeightControl.valueChanged.connect(lambda v: self.saveAndUpdate("lineWeight", v, self.instrument.setLineWeight))
        self.dotSizeControl.valueChanged.connect(lambda v: self.saveAndUpdate("dotSize", v, self.instrument.setDotSize))
        self.outlineWeightControl.valueChanged.connect(lambda v: self.saveAndUpdate("outlineWeight", v, self.instrument.setOutlineWeight))
        self.wingsDistanceControl.valueChanged.connect(lambda v: self.saveAndUpdate("wingsDistance", v, self.instrument.setWingsDistance))
        self.wingsSpanControl.valueChanged.connect(lambda v: self.saveAndUpdate("wingsSpan", v, self.instrument.setWingsSpan))
        self.wingsHeightControl.valueChanged.connect(lambda v: self.saveAndUpdate("wingsHeight", v, self.instrument.setWingsHeight))

        planeLayout.addWidget(self.lineWeightControl)
        planeLayout.addWidget(self.dotSizeControl)
        planeLayout.addWidget(self.outlineWeightControl)
        planeLayout.addWidget(self.wingsDistanceControl)
        planeLayout.addWidget(self.wingsSpanControl)
        planeLayout.addWidget(self.wingsHeightControl)
        
        mainLayout.addWidget(planeGroup)

    def saveAndUpdate(self, key, value, callbackFunc):
        self.settings.setValue(key, value)
        self.settings.sync()
        callbackFunc(value)

    def createSection(self, title):
        group = QGroupBox(title)
        layout = QVBoxLayout(group)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        return group, layout