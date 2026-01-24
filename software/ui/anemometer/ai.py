from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsPolygonItem
from PyQt6.QtGui import QColor, QPen, QPolygonF
from PyQt6.QtCore import Qt, QPointF

class SpeedAi(QGraphicsItemGroup):
    def __init__(self, parent=None):
        super().__init__(parent)
        size=600

        indicator = QGraphicsPolygonItem()
        self.addToGroup(indicator)

        polygon = QPolygonF([
            QPointF(60, -10),
            QPointF(60, 10),
            QPointF(40, 10),
            QPointF(25, 0),
            QPointF(40, -10),
        ])

        indicator.setPolygon(polygon)
        indicator.setPen(QPen(QColor("#FF00FF"), 3))
    
    def updatePositions(self, speed, aimedSpeed):
        knotsPerGraduation = 10
        pixelsPerGraduation = 34
        pxPerKnot = pixelsPerGraduation / knotsPerGraduation

        offset=(speed-aimedSpeed)*pxPerKnot
        if offset>205 :
            offset=205
        elif offset<-205 :
            offset=-205
        self.setPos(0, offset)