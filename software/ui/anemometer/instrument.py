from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsRectItem, QGraphicsItem, QGraphicsLineItem
from PyQt6.QtGui import QBrush, QColor, QPen, QPainterPath
from PyQt6.QtCore import Qt, QRectF

from ui.anemometer.graduations import SpeedGraduations
from ui.anemometer.indicator import SpeedIndicator
from ui.anemometer.ai import SpeedAi

class AnemometerInstrument(QGraphicsItemGroup):
    def __init__(self):
        super().__init__()
        self.width = 70
        self.height = 410

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemClipsChildrenToShape, True)

        self.rect = QGraphicsRectItem(
            -self.width / 2, -self.height / 2,
            self.width, self.height
        )
        
        self.rect.setBrush(QBrush(QColor("#808080")))
        self.rect.setPen(QPen(Qt.PenStyle.NoPen))
        self.addToGroup(self.rect)

        self.setTransformOriginPoint(0, 0)

        self.graduations = SpeedGraduations(parent=self, width=self.width)
        self.addToGroup(self.graduations)

        self.ai = SpeedAi(parent=self)
        self.addToGroup(self.ai)

        self.indicator = SpeedIndicator(parent=self)
        self.addToGroup(self.indicator)

    def updatePositions(self, speed):
        self.graduations.updatePositions(speed)
        self.indicator.updatePositions(speed)
        self.ai.updatePositions(speed,260)

    def boundingRect(self,width=70,height=410):
        return QRectF(-width, -height / 2, width*2, height)

    def shape(self):
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path