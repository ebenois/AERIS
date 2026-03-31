from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsRectItem
from PyQt6.QtGui import QBrush, QColor, QPen
from PyQt6.QtCore import Qt, QSettings
import numbers

from ui.altimeter.graduations import AltitudeGraduations
from ui.altimeter.indicator import AltitudeIndicator
from ui.altimeter.trend import AltitudeTrend
from ui.altimeter.limit import AltitudeLimit


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

        self.rect = QGraphicsRectItem(0, 0, self.width, self.height)
        self.rect.setBrush(QBrush(QColor("#808080")))
        self.rect.setPen(QPen(Qt.PenStyle.NoPen))
        self.addToGroup(self.rect)

        self.alertFrame = QGraphicsRectItem(0, 0, self.width, self.height)
        self.isInErrorPen = QPen(QColor("red"), 10)
        self.isCriticalPen = QPen(QColor("#ff7f00"), 10)
        self.alertFrame.setVisible(False)

        self.limit = AltitudeLimit(width, height, self.limitmax)
        self.trend = AltitudeTrend(width, height)
        self.graduations = AltitudeGraduations(width, height)
        self.indicator = AltitudeIndicator(width, height)

        for item in [
            self.limit,
            self.trend,
            self.graduations,
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

    def drawAlert(self, flashOpacity):
        if self.isInError:
            self.alertFrame.setPen(self.isInErrorPen)
            self.alertFrame.setVisible(True)
            self.alertFrame.setOpacity(flashOpacity)

            self.graduations.hide()
            self.trend.hide()
            self.limit.hide()
            self.indicator.updatePositions("ERR")

        elif self.isCritical:
            self.alertFrame.setPen(self.isCriticalPen)
            self.alertFrame.setVisible(True)
            self.alertFrame.setOpacity(0.5 + 0.5 * flashOpacity)

        else:
            self.graduations.show()
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
            altitude = pressure_to_altitude(pressure, self.qnh)
            
            self.graduations.updatePositions(altitude)
            self.indicator.updatePositions(altitude)
            self.limit.updatePositions(altitude)
            
            if isinstance(windSpeed, numbers.Number) and isinstance(
                pitch, numbers.Number
            ):
                self.trend.updatePositions(windSpeed, pitch)
                
            if altitude <= self.limitmin or altitude >= self.limitmax:
                self.isCritical = True
            else:
                self.isCritical = False
        else:
            self.isInError = True

def pressure_to_altitude(pression_hpa, qnh_hpa=1013.25):
    if pression_hpa <= 0: return 0
    return 44330.0 * (1.0 - (pression_hpa / qnh_hpa) ** 0.1903)