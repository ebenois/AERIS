from PyQt6.QtWidgets import (
    QGraphicsItemGroup,
    QGraphicsRectItem,
    QGraphicsItem,
    QGraphicsLineItem,
)
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

        self.noDataEffect = QPen(Qt.PenStyle.NoPen)
        self.rect.setPen(self.noDataEffect)

        self.limit = SpeedLimit(width, height)
        self.addToGroup(self.limit)

        self.trend = SpeedTrend(width, height)
        self.addToGroup(self.trend)

        self.graduations = SpeedGraduations(width, height)
        self.addToGroup(self.graduations)

        self.indicator = SpeedIndicator(width, height)
        self.addToGroup(self.indicator)

        self.isInError = False
        
        self.updatePositions((0,0,0,0,0,40,0,0,0))

    def drawAlert(self, showRed):
        if showRed and self.isInError:
            self.rect.setPen(QPen(QColor("red"), 15))
        else:
            self.rect.setPen(QPen(Qt.PenStyle.NoPen))

    def updatePositions(self, data):
        packetId,roll,pitch,altitude,climbRate,windSpeed,heading,slip,button = data
        if isinstance(windSpeed, numbers.Number):
            self.isInError = False
            self.graduations.updatePositions(windSpeed)
            self.indicator.updatePositions(windSpeed)
            self.limit.updatePositions(windSpeed)
            self.trend.updatePositions(windSpeed)
        else:
            self.isInError = True
            self.indicator.updatePositions("Err")
