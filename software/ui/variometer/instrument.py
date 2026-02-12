from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsRectItem, QGraphicsItem, QGraphicsLineItem
from PyQt6.QtGui import QBrush, QColor, QPen, QPainterPath
from PyQt6.QtCore import Qt, QRectF

from ui.variometer.graduations import RiseGraduations
from ui.variometer.indicator import RiseIndicator

class VariometerInstrument(QGraphicsItemGroup):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemClipsChildrenToShape, True)

        self.rect = QGraphicsRectItem(
            0, 0,
            self.width, self.height
        )
        
        self.rect.setBrush(QBrush(QColor("#808080")))
        self.rect.setPen(QPen(Qt.PenStyle.NoPen))
        self.addToGroup(self.rect)

        self.setTransformOriginPoint(0, 0)

        self.graduations = RiseGraduations(width, height)
        self.addToGroup(self.graduations)

        self.indicator = RiseIndicator(width, height)
        self.addToGroup(self.indicator)
        self.indicator.setPos(width*2/3,height/2)

    def updatePositions(self, altitude):
        self.indicator.updatePositions(altitude)

    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)

    def shape(self):
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path