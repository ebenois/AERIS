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

        self.setTransformOriginPoint(0, 0)

        self.graduations = SpeedGraduations(width,height)
        self.addToGroup(self.graduations)

        self.indicator = SpeedIndicator(width,height)
        self.addToGroup(self.indicator)

    def updatePositions(self, speed):
        if (isinstance(speed, numbers.Number)):
            self.graduations.updatePositions(speed)
            self.indicator.updatePositions(speed)
        
    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)

    def shape(self):
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path