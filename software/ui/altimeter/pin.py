from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsPolygonItem
from PyQt6.QtGui import QColor, QPen, QPolygonF
from PyQt6.QtCore import Qt, QPointF

class AltitudePin(QGraphicsItemGroup):
    def __init__(self, width, height):
        super().__init__()
        
        self.span = 500
        self.height = height
        self.pixelPerUnit = (self.height / 2) / self.span
        self.width = width

        indicator = QGraphicsPolygonItem()
        self.addToGroup(indicator)

        polygon = QPolygonF([
            QPointF(15, -25),
            QPointF(-15, -25),
            QPointF(-15, 25),
            QPointF(15, 25),
            QPointF(15, 10),
            QPointF(10, 0),
            QPointF(15, -10),
        ])

        indicator.setPolygon(polygon)
        indicator.setPen(QPen(QColor("#FF00FF"), 3))
    
    def updatePositions(self, altitude, aimedAltitude):
        heightPx = (aimedAltitude - altitude) * self.pixelPerUnit
        safe = max(-self.height / 2, min(self.height / 2, heightPx))
        self.setPos(0, self.height / 2 - safe)