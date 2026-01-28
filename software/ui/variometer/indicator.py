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
        # On utilise la même formule que les graduations : log10(abs(x) + 1)
        # math.copysign permet de garder le signe (montée/descente)
        pxPerUnit = 145
        
        offset = math.log10(abs(rise) + 1)
        pixels = math.copysign(offset * pxPerUnit, rise)

        # On limite le mouvement au span (6)
        max_y = math.log10(6 + 1) * pxPerUnit
        pixels = max(-max_y, min(max_y, pixels))

        self.setPos(0, -pixels)