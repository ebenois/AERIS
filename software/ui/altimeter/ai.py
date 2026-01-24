from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsPolygonItem
from PyQt6.QtGui import QColor, QPen, QPolygonF
from PyQt6.QtCore import Qt, QPointF

class AltitudeAi(QGraphicsItemGroup):
    def __init__(self, parent=None):
        super().__init__(parent)
        size=600

        indicator = QGraphicsPolygonItem()
        self.addToGroup(indicator)

        polygon = QPolygonF([
            QPointF(-50, -25),
            QPointF(-20, -25),
            QPointF(-20, 25),
            QPointF(-50, 25),
            QPointF(-50, 10),
            QPointF(-35, 0),
            QPointF(-50, -10),
        ])

        indicator.setPolygon(polygon)
        indicator.setPen(QPen(QColor("#FF00FF"), 3))
    
    def updatePositions(self, altitude, aimedAltitude):
        metersPerGraduation = 100
        pixelsPerGraduation = 48
        pxPerMeter = pixelsPerGraduation / metersPerGraduation

        offset=(altitude-aimedAltitude)*pxPerMeter
        if offset>205 :
            offset=205
        elif offset<-205 :
            offset=-205
        print(offset)
        self.setPos(0, offset)