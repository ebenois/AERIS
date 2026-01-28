from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsRectItem, QGraphicsItem, QGraphicsLineItem
from PyQt6.QtGui import QBrush, QColor, QPen, QPainterPath
from PyQt6.QtCore import Qt, QRectF

from ui.variometer.graduations import RiseGraduations
from ui.variometer.indicator import RiseIndicator

class VariometerInstrument(QGraphicsItemGroup):
    def __init__(self):
        super().__init__()
        self.width = 48
        self.height = 260

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemClipsChildrenToShape, True)

        self.rect = QGraphicsRectItem(
            -self.width / 2, -self.height / 2,
            self.width, self.height
        )
        
        self.rect.setBrush(QBrush(QColor("#808080")))
        self.rect.setPen(QPen(Qt.PenStyle.NoPen))
        self.addToGroup(self.rect)

        self.setTransformOriginPoint(0, 0)

        self.graduations = RiseGraduations(parent=self, width=self.width)
        self.addToGroup(self.graduations)

        self.indicator = RiseIndicator(parent=self)
        self.addToGroup(self.indicator)

    def updatePositions(self, altitude):
        self.indicator.updatePositions(altitude)

    def boundingRect(self):
        return QRectF(-self.width, -self.height / 2, self.width*2, self.height)

    def shape(self):
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path