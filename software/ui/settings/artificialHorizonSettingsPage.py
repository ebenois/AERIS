from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGroupBox,
)
from PyQt6.QtCore import Qt, QSettings

from ui.settings.settingGroup import SettingGroup


class ArtificialHorizonSettingsPage(QWidget):
    def __init__(self, instrument):
        super().__init__()
        self.settings = QSettings("ENSC", "AERIS")
        self.instrument = instrument

        mainLayout = QVBoxLayout(self)

        planeGroup, planeLayout = self.createSection("Avion")
        backgroundGroup, backgroundLayout = self.createSection("Fond")
        graduationsGroup, graduationsLayout = self.createSection("Graduations")

        lineWeight = self.settings.value("lineWeight", 10, int)
        dotSize = self.settings.value("dotSize", 10, int)
        outlineWeight = self.settings.value("outlineWeight", 5, int)
        wingsDistance = self.settings.value("wingsDistance", 45, int)
        wingsSpan = self.settings.value("wingsSpan", 75, int)
        wingsHeight = self.settings.value("wingsHeight", 12, int)

        self.lineWeightControl = SettingGroup("Line weight", 0, 50, lineWeight, 10)
        self.dotSizeControl = SettingGroup("Dot size", 0, 50, dotSize, 10)
        self.outlineWeightControl = SettingGroup(
            "Outline weight", 0, 50, outlineWeight, 10
        )
        self.wingsDistanceControl = SettingGroup(
            "Distance between wings", 1, 100, wingsDistance, 20
        )
        self.wingsSpanControl = SettingGroup("Wings span", 1, 200, wingsSpan, 20)
        self.wingsHeightControl = SettingGroup("Wings height", 1, 100, wingsHeight, 20)

        self.lineWeightControl.valueChanged.connect(
            lambda v: self.saveAndUpdate("lineWeight", v, self.instrument.setLineWeight)
        )
        self.dotSizeControl.valueChanged.connect(
            lambda v: self.saveAndUpdate("dotSize", v, self.instrument.setDotSize)
        )
        self.outlineWeightControl.valueChanged.connect(
            lambda v: self.saveAndUpdate(
                "outlineWeight", v, self.instrument.setOutlineWeight
            )
        )
        self.wingsDistanceControl.valueChanged.connect(
            lambda v: self.saveAndUpdate(
                "wingsDistance", v, self.instrument.setWingsDistance
            )
        )
        self.wingsSpanControl.valueChanged.connect(
            lambda v: self.saveAndUpdate("wingsSpan", v, self.instrument.setWingsSpan)
        )
        self.wingsHeightControl.valueChanged.connect(
            lambda v: self.saveAndUpdate(
                "wingsHeight", v, self.instrument.setWingsHeight
            )
        )

        planeLayout.addWidget(self.lineWeightControl)
        planeLayout.addWidget(self.dotSizeControl)
        planeLayout.addWidget(self.outlineWeightControl)
        planeLayout.addWidget(self.wingsDistanceControl)
        planeLayout.addWidget(self.wingsSpanControl)
        planeLayout.addWidget(self.wingsHeightControl)

        mainLayout.addWidget(planeGroup)
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
