from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsRectItem
from PyQt6.QtGui import QBrush, QColor, QPen
from PyQt6.QtCore import Qt
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
        self.limitmax = 3900
        self.limitmin = 1000
        
        self.isInError = True
        self.isCritical = False

        self.rect = QGraphicsRectItem(0, 0, self.width, self.height)
        self.rect.setBrush(QBrush(QColor("#808080")))
        self.rect.setPen(QPen(Qt.PenStyle.NoPen))
        self.addToGroup(self.rect)

        self.alertFrame = QGraphicsRectItem(0, 0, self.width, self.height)
        self.isInErrorPen = QPen(QColor("red"), 10)
        self.isCriticalPen = QPen(QColor("#ff7f00"), 10)
        self.alertFrame.setVisible(False)
        self.addToGroup(self.alertFrame)

        self.limit = AltitudeLimit(width, height, self.limitmax)
        self.trend = AltitudeTrend(width, height)
        self.graduations = AltitudeGraduations(width, height)
        self.indicator = AltitudeIndicator(width, height)

        for item in [self.limit, self.trend, self.graduations, self.indicator]:
            self.addToGroup(item)

    def drawAlert(self, flashOn):
        if self.isInError:
            self.alertFrame.setPen(self.isInErrorPen)
            self.alertFrame.setVisible(flashOn)

            self.graduations.hide()
            self.trend.hide()
            self.limit.hide()
            self.indicator.updatePositions("ERR")
            
        elif self.isCritical:
            self.alertFrame.setPen(self.isCriticalPen)
            self.alertFrame.setVisible(flashOn)

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

    def updatePositions(self, pitch, altitude, windSpeed):
        data_valid = isinstance(altitude, (int, float))

        if data_valid:
            self.isInError = False
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