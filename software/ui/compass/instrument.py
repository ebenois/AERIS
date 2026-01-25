from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsEllipseItem, QGraphicsPolygonItem
from PyQt6.QtGui import QBrush, QColor, QPen, QPolygonF
from PyQt6.QtCore import Qt, QPointF

from ui.compass.graduations import DirectionGraduations
from ui.compass.ai import DirectionAi

class CompassInstrument(QGraphicsItemGroup):
    def __init__(self):
        super().__init__()

        radius = 222
        dot = QGraphicsEllipseItem(-radius, -radius, radius*2, radius*2)
        dot.setBrush(QBrush(QColor("#808080")))
        dot.setPen(QPen(Qt.PenStyle.NoPen))
        self.addToGroup(dot)

        self.graduations = DirectionGraduations()
        self.addToGroup(self.graduations)

        self.ai = DirectionAi(parent=self)
        self.addToGroup(self.ai)

        indicator = QGraphicsPolygonItem()
        self.addToGroup(indicator)

        width = 40
        radius = 223
        length = 10

        polygon = QPolygonF([
            QPointF(0, -radius),
            QPointF(length, -(radius+width/2)),
            QPointF(-length, -(radius+width/2)),
        ])

        indicator.setPolygon(polygon)
        indicator.setBrush(QBrush(Qt.GlobalColor.black))
        indicator.setPen(QPen(Qt.GlobalColor.white, 3))

    def updatePositions(self, direction):
        self.graduations.updatePositions(direction)
        self.ai.updatePositions(direction,250)