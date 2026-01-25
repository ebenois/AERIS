from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsEllipseItem
from PyQt6.QtGui import QBrush, QColor, QPen
from PyQt6.QtCore import Qt

from ui.compass.graduations import DirectionGraduations

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

    def updatePositions(self, direction):
        self.graduations.updatePositions(direction)