from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsPolygonItem
from PyQt6.QtGui import QColor, QPen, QPolygonF
from PyQt6.QtCore import Qt, QPointF

class DirectionAi(QGraphicsItemGroup):
    def __init__(self, parent=None):
        super().__init__(parent)

        indicator = QGraphicsPolygonItem()
        self.addToGroup(indicator)

        width = 20
        radius = 223
        length = 10

        polygon = QPolygonF([
            QPointF(-length, -radius),
            QPointF(length, -radius),
            QPointF(length, -(radius+width/2)),
            QPointF(0, -(radius)),
            QPointF(-length, -(radius+width/2)),
        ])

        indicator.setPolygon(polygon)
        indicator.setPen(QPen(QColor("#FF00FF"), 3))
    
    def updatePositions(self, angle, aimedAngle):
        maxOffset = 60
        offset=aimedAngle-angle
        if offset>maxOffset :
            offset=maxOffset
        elif offset<-maxOffset :
            offset=-maxOffset
        self.setRotation(offset)