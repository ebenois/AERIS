from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsRectItem
from PyQt6.QtGui import QBrush, QColor, QPen
from PyQt6.QtCore import Qt
import numbers

from ui.anemometer.graduations import SpeedGraduations
from ui.anemometer.indicator import SpeedIndicator
from ui.anemometer.trend import SpeedTrend
from ui.anemometer.limit import SpeedLimit


class AnemometerInstrument(QGraphicsItemGroup):
    def __init__(self, width, height):
        super().__init__()
        self.height = height
        self.width = width

        self.rect = QGraphicsRectItem(0, 0, width, height)
        self.rect.setBrush(QBrush(QColor("#808080")))
        self.rect.setPen(QPen(Qt.PenStyle.NoPen))
        self.addToGroup(self.rect)

        self.alertFrame = QGraphicsRectItem(0, 0, self.width, self.height)
        self.alertFrame.setPen(QPen(QColor("red"), 10))
        self.alertFrame.setVisible(False)
        self.addToGroup(self.alertFrame)

        self.limit = SpeedLimit(width, height)
        self.trend = SpeedTrend(width, height)
        self.graduations = SpeedGraduations(width, height)
        self.indicator = SpeedIndicator(width, height)

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

    def updatePositions(self, windSpeed):
        dataValid = isinstance(windSpeed, numbers.Number)

        if dataValid:
            self.isInError = False
            self.graduations.updatePositions(windSpeed)
            self.indicator.updatePositions(windSpeed)
            self.limit.updatePositions(windSpeed)
            self.trend.updatePositions(windSpeed)
        else:
            self.isInError = True
