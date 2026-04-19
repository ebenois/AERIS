from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsRectItem
from PyQt6.QtGui import QBrush, QColor, QPen
from PyQt6.QtCore import Qt, QSettings

from ui.altimeter.graduations import AltitudeGraduations
from ui.altimeter.indicator import AltitudeIndicator
from ui.altimeter.trend import AltitudeTrend
from ui.altimeter.limit import AltitudeLimit
from ui.altimeter.pin import AltitudePin


class AltimeterInstrument(QGraphicsItemGroup):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height

        self.isInError = True
        self.isCritical = False

        self.settings = QSettings("ENSC", "AERIS")
        self.qnh = int(self.settings.value("QNH", 1013))
        self.limitmax = int(self.settings.value("limitMax", 1000))
        self.limitmin = int(self.settings.value("limitMin", 10))
        self.wantedAltitude = int(self.settings.value("wantedAltitude", 100))
        self.altitudeUnit = self.settings.value("altitudeUnit", "km")

        self.rect = QGraphicsRectItem(0, 0, self.width, self.height)
        self.rect.setBrush(QBrush(QColor("#808080")))
        self.rect.setPen(QPen(Qt.PenStyle.NoPen))
        self.addToGroup(self.rect)

        self.alertFrame = QGraphicsRectItem(0, 0, self.width, self.height)
        self.isInErrorPen = QPen(QColor("red"), 10)
        self.isCriticalPen = QPen(QColor("#ff7f00"), 10)
        self.alertFrame.setVisible(False)

        self.limit = AltitudeLimit(width, height)
        self.trend = AltitudeTrend(width, height)
        self.graduations = AltitudeGraduations(width, height)
        self.indicator = AltitudeIndicator(width, height)
        self.pin = AltitudePin(width, height)

        for item in [
            self.limit,
            self.trend,
            self.graduations,
            self.pin,
            self.alertFrame,
            self.indicator,
        ]:
            self.addToGroup(item)

    def setQNH(self, value):
        self.qnh = value

    def setAltitudeMax(self, value):
        self.limitmax = value

    def setAltitudeMin(self, value):
        self.limitmin = value

    def setAltitudePin(self, value):
        self.wantedAltitude = value
        
    def setAltitudeUnit(self, value):
        self.altitudeUnit = value

    def drawAlert(self, flashOpacity):
        if self.isInError:
            self.alertFrame.setPen(self.isInErrorPen)
            self.alertFrame.setVisible(True)
            self.alertFrame.setOpacity(flashOpacity)

            self.graduations.hide()
            self.pin.hide()
            self.trend.hide()
            self.limit.hide()
            self.indicator.updatePositions("ERR")

        elif self.isCritical:
            self.alertFrame.setPen(self.isCriticalPen)
            self.alertFrame.setVisible(True)
            self.alertFrame.setOpacity(0.5 + 0.5 * flashOpacity)

        else:
            self.graduations.show()
            self.pin.show()
            self.trend.show()
            self.limit.show()
            self.alertFrame.setVisible(False)

    def drawLess(self, highMentalLoad):
        if highMentalLoad:
            self.setOpacity(0.5)
        else:
            self.setOpacity(1)

    def updatePositions(self, pitch, pressure, windSpeed):
        data_valid = isinstance(pressure, (int, float))

        if data_valid:
            self.isInError = False
            altitude = self.pressure_to_altitude(pressure, self.qnh)
            altitudeChanged = self.changeUnit(altitude, self.altitudeUnit)

            self.graduations.updatePositions(altitude)
            self.indicator.updatePositions(altitudeChanged)

            self.limit.updatePositions(altitude, self.limitmax)
            self.trend.updatePositions(windSpeed, pitch)
            self.pin.updatePositions(altitude, self.wantedAltitude)

            if altitude <= self.limitmin or altitude >= self.limitmax:
                self.isCritical = True
            else:
                self.isCritical = False
        else:
            self.isInError = True


    def pressure_to_altitude(self, pression_hpa, qnh_hpa=1013.25):
        if pression_hpa <= 0:
            return 0
        return 44330.0 * (1.0 - (pression_hpa / qnh_hpa) ** 0.1903)

    def changeUnit(self, altitude, altitudeUnit):
        if (altitudeUnit == "km"):
            return altitude
        elif (altitudeUnit == "hm"):
            return altitude*10
        elif (altitudeUnit == "dam"):
            return altitude*100
        else:
            return altitude*1000
