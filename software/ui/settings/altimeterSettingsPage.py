import sys
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QSpinBox,
    QGroupBox,
    QComboBox,
)
from PyQt6.QtCore import Qt, QSettings


class AltimeterSettingsPage(QWidget):
    def __init__(self, instrument):
        super().__init__()
        self.settings = QSettings("ENSC", "AERIS")
        self.instrument = instrument

        mainLayout = QVBoxLayout(self)

        calibrationGroup, calibrationLayout = self.createSection("Calibration")

        qnhLayout = QHBoxLayout()
        qnhLabel = QLabel("QNH (hPa) :")

        self.qnhSpin = QSpinBox()
        self.qnhSpin.setRange(900, 1100)
        self.qnhSpin.setSingleStep(1)

        currentQNH = int(self.settings.value("QNH", 1013))
        self.qnhSpin.setValue(currentQNH)

        self.qnhSpin.valueChanged.connect(
            lambda v: self.saveAndUpdate("QNH", v, self.instrument.setQNH)
        )

        qnhLayout.addWidget(qnhLabel)
        qnhLayout.addWidget(self.qnhSpin)
        calibrationLayout.addLayout(qnhLayout)
        mainLayout.addWidget(calibrationGroup)

        altitudeGroup, altitudeLayout = self.createSection("Altitude de vol (m)")

        minLayout = QHBoxLayout()
        minLabel = QLabel("Altitude min :")
        self.minSpin = QSpinBox()
        self.minSpin.setRange(0, 20000)
        self.minSpin.setSingleStep(10)
        currentMin = int(self.settings.value("limitMin", 10))
        self.minSpin.setValue(currentMin)
        self.minSpin.valueChanged.connect(
            lambda v: self.saveAndUpdate("limitMin", v, self.instrument.setAltitudeMin)
        )
        minLayout.addWidget(minLabel)
        minLayout.addWidget(self.minSpin)
        altitudeLayout.addLayout(minLayout)

        maxLayout = QHBoxLayout()
        maxLabel = QLabel("Altitude max :")
        self.maxSpin = QSpinBox()
        self.maxSpin.setRange(0, 20000)
        self.maxSpin.setSingleStep(10)
        currentMax = int(self.settings.value("limitMax", 1000))
        self.maxSpin.setValue(currentMax)
        self.maxSpin.valueChanged.connect(
            lambda v: self.saveAndUpdate("limitMax", v, self.instrument.setAltitudeMax)
        )
        maxLayout.addWidget(maxLabel)
        maxLayout.addWidget(self.maxSpin)
        altitudeLayout.addLayout(maxLayout)
        mainLayout.addWidget(altitudeGroup)

        indicatorGroup, indicatorLayout = self.createSection("Indicateur")

        unitLayout = QHBoxLayout()
        unitLabel = QLabel("Unité :")
        self.unitCombo = QComboBox()
        self.unitCombo.addItems(["m", "dam", "hm", "km"])
        currentUnit = self.settings.value("altitudeUnit", "m")
        self.unitCombo.setCurrentText(currentUnit)
        self.unitCombo.currentTextChanged.connect(
            lambda v: self.saveAndUpdate("altitudeUnit", v, self.instrument.setAltitudeUnit)
        )

        unitLayout.addWidget(unitLabel)
        unitLayout.addWidget(self.unitCombo)

        indicatorLayout.addLayout(unitLayout)
        
        limitLabel = QLabel("Altitude désirée (m) :")

        self.limitSpin = QSpinBox()
        self.limitSpin.setRange(0, 2000)
        self.limitSpin.setSingleStep(1)

        currentLimit = int(self.settings.value("wantedAltitude", 100))
        self.limitSpin.setValue(currentLimit)

        self.limitSpin.valueChanged.connect(
            lambda v: self.saveAndUpdate(
                "wantedAltitude", v, self.instrument.setAltitudePin
            )
        )

        limitLayout = QHBoxLayout()
        limitLayout.addWidget(limitLabel)
        limitLayout.addWidget(self.limitSpin)
        altitudeLayout.addLayout(limitLayout)
        mainLayout.addWidget(indicatorGroup)

        mainLayout.addStretch()

    def saveAndUpdate(self, key, value, callbackFunc):
        self.settings.setValue(key, value)
        self.settings.sync()

        if callable(callbackFunc):
            callbackFunc(value)

    def createSection(self, title):
        group = QGroupBox(title)
        layout = QVBoxLayout(group)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        return group, layout
