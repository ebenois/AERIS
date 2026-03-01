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

        self.rect = QGraphicsRectItem(0, 0, self.width, self.height)
        self.rect.setBrush(QBrush(QColor("#808080")))
        self.rect.setPen(QPen(Qt.PenStyle.NoPen))
        self.addToGroup(self.rect)

        self.alertFrame = QGraphicsRectItem(0, 0, self.width, self.height)
        self.alertFrame.setPen(QPen(QColor("red"), 10))
        self.alertFrame.setVisible(False)
        self.addToGroup(self.alertFrame)

        self.limit = AltitudeLimit(width, height)
        self.trend = AltitudeTrend(width, height)
        self.graduations = AltitudeGraduations(width, height)
        self.indicator = AltitudeIndicator(width, height)

        for item in [self.limit, self.trend, self.graduations, self.indicator]:
            self.addToGroup(item)

        self.isInError = True

    def drawAlert(self, flashOn):
        if self.isInError:
            self.alertFrame.setVisible(flashOn)
            self.graduations.hide()
            self.trend.hide()
            self.limit.hide()
            self.indicator.updatePositions("ERR")
        else:
            self.alertFrame.setVisible(False)
            self.graduations.show()
            self.trend.show()
            self.limit.show()

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
        else:
            self.isInError = True
