import sys
from PyQt6.QtWidgets import (
    QWidget, 
    QLabel, 
    QVBoxLayout, 
    QHBoxLayout, 
    QSlider, 
    QPushButton
)
from PyQt6.QtCore import Qt, QSettings, pyqtSignal

from ui.settings.settingGroup import SettingGroup

class SettingsPage(QWidget):
    def __init__(self, instrument):
        super().__init__()
        self.settings = QSettings("ENSC", "AERIS")
        self.instrument = instrument

        mainLayout = QVBoxLayout(self)
        mainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.lineWeightControl = SettingGroup("Line Weight", 1, 30, 10)
        self.lineWeightControl.valueChanged.connect(lambda v: self.saveAndUpdate("lineWeight", v, self.instrument.setLineWeight))
        mainLayout.addWidget(self.lineWeightControl)

        self.dotSizeControl = SettingGroup("Dot Size", 1, 30, 10)
        self.dotSizeControl.valueChanged.connect(lambda v: self.saveAndUpdate("dotSize", v, self.instrument.setDotSize))
        mainLayout.addWidget(self.dotSizeControl)

        self.outlineWeightControl = SettingGroup("outline Weight", 1, 15, 5)
        self.outlineWeightControl.valueChanged.connect(lambda v: self.saveAndUpdate("outlineWeight", v, self.instrument.setOutlineWeight))
        mainLayout.addWidget(self.outlineWeightControl)

        self.loadAllValues()

    def saveAndUpdate(self, key, value, callbackFunc):
        self.settings.setValue(key, value)
        callbackFunc(value)

    def loadAllValues(self):
        lineWeight = self.settings.value("lineWeight", 10, int)
        self.lineWeightControl.setValue(lineWeight)
        self.instrument.setLineWeight(lineWeight)

        dotSize = self.settings.value("dotSize", 10, int)
        self.dotSizeControl.setValue(dotSize)
        self.instrument.setDotSize(dotSize)