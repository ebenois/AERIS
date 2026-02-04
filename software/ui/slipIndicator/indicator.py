from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsLineItem, QGraphicsTextItem, QGraphicsRectItem, QGraphicsItem, QGraphicsPolygonItem
from PyQt6.QtGui import QColor, QPen, QFont, QBrush, QPainterPath, QPolygonF
from PyQt6.QtCore import Qt, QRectF, QPointF
import math

class SlipIndicator(QGraphicsItemGroup):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.width = 30
        self.height = 15

        triangle = QGraphicsPolygonItem()
        self.addToGroup(triangle)

        polygon = QPolygonF([
            QPointF(0, -135),
            QPointF(self.width/2, -135+self.height),
            QPointF(-self.width/2, -135+self.height),
        ])

        triangle.setPolygon(polygon)
        triangle.setBrush(QBrush(Qt.GlobalColor.white))
        triangle.setPen(QPen(Qt.PenStyle.NoPen))

    def updatePositions(self, slip):
        maxRotation = 60
        pixels = max(-maxRotation, min(maxRotation, slip))

        self.setRotation(slip)