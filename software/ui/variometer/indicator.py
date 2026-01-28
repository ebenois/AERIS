from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsLineItem, QGraphicsTextItem, QGraphicsRectItem, QGraphicsItem, QGraphicsPolygonItem
from PyQt6.QtGui import QColor, QPen, QFont, QBrush, QPainterPath, QPolygonF
from PyQt6.QtCore import Qt, QRectF, QPointF
import math

class RiseIndicator(QGraphicsItemGroup):
    def __init__(self, parent=None, width=30, height=20):
        super().__init__(parent)
        self.width = width
        self.height = height

        triangle = QGraphicsPolygonItem()
        self.addToGroup(triangle)

        polygon = QPolygonF([
            QPointF(0, 0),
            QPointF(width/2, -height/2),
            QPointF(width/2, height/2),
        ])

        triangle.setPolygon(polygon)
        triangle.setBrush(QBrush(Qt.GlobalColor.black))
        triangle.setPen(QPen(Qt.GlobalColor.white, 3))

    def updatePositions(self, rise):
        print(rise)
        if abs(rise) < 1:
            offset = 0
        else:
            offset = math.copysign(math.log10(abs(rise)), rise)

        print(offset)

        offset = max(-6, min(6, offset))

        pixels = offset/math.log10(6) * 125

        self.setPos(0, -pixels)
