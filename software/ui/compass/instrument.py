from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsEllipseItem, QGraphicsPolygonItem
from PyQt6.QtGui import QBrush, QColor, QPen, QPolygonF
from PyQt6.QtCore import Qt, QPointF
import numbers

from ui.compass.graduations import DirectionGraduations

class CompassInstrument(QGraphicsItemGroup):
    def __init__(self, width, heigth):
        super().__init__()

        dot = QGraphicsEllipseItem(0, 0, width, heigth)
        dot.setBrush(QBrush(QColor("#808080")))
        dot.setPen(QPen(Qt.PenStyle.NoPen))
        self.addToGroup(dot)

        self.graduations = DirectionGraduations(width)
        self.addToGroup(self.graduations)
        self.graduations.setPos(width/2, heigth/2)

        indicator = QGraphicsPolygonItem()
        self.addToGroup(indicator)

        polygonWidth = 55
        polygonHeigth = 45

        polygon = QPolygonF([
            QPointF(width/2, 0),
            QPointF(width/2+polygonWidth/2, -(polygonHeigth)),
            QPointF(width/2-polygonWidth/2, -(polygonHeigth)),
        ])

        indicator.setPolygon(polygon)
        indicator.setBrush(QBrush(Qt.GlobalColor.black))
        indicator.setPen(QPen(Qt.GlobalColor.white, 3))

    def updatePositions(self, direction):
        if (isinstance(direction, numbers.Number)):
            self.graduations.updatePositions(direction)