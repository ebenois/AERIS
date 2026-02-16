from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsRectItem, QGraphicsItem, QGraphicsLineItem
from PyQt6.QtGui import QBrush, QColor, QPen, QPainterPath
from PyQt6.QtCore import Qt, QRectF
import numbers

from ui.anemometer.graduations import SpeedGraduations
from ui.anemometer.indicator import SpeedIndicator


class AnemometerInstrument(QGraphicsItemGroup):
    def __init__(self, width, height):
        super().__init__()

        self.height = height
        self.width = width

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemClipsChildrenToShape, True)

        self.rect = QGraphicsRectItem(
            0, 0,
            width, height
        )
        
        self.rect.setBrush(QBrush(QColor("#808080")))
        self.rect.setPen(QPen(Qt.PenStyle.NoPen))
        self.addToGroup(self.rect)

        self.noDataEffect = QPen(Qt.PenStyle.NoPen)
        self.rect.setPen(self.noDataEffect)

        self.graduations = SpeedGraduations(width,height)
        self.addToGroup(self.graduations)

        self.indicator = SpeedIndicator(width,height)
        self.addToGroup(self.indicator)

        self.isInError = False 

    def drawAlert(self, showRed):
        if showRed and self.isInError:
            self.rect.setPen(QPen(QColor("red"), 15))
        else:
            self.rect.setPen(QPen(Qt.PenStyle.NoPen))

    def updatePositions(self, speed):
        if isinstance(speed, numbers.Number):
            self.isInError = False
            self.graduations.updatePositions(speed)
            self.indicator.updatePositions(speed)
        else:
            self.isInError = True
            self.indicator.updatePositions("Err")
        
    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)

    def shape(self):
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path