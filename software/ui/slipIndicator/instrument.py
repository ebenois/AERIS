from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsEllipseItem, QGraphicsPolygonItem
from PyQt6.QtGui import QBrush, QColor, QPen, QPolygonF
from PyQt6.QtCore import Qt, QPointF

from ui.slipIndicator.graduations import SlipGraduations
from ui.slipIndicator.indicator import SlipIndicator

class SlipInstrument(QGraphicsItemGroup):
    def __init__(self):
        super().__init__()

        width=25
        height=15

        self.graduations = SlipGraduations()
        self.addToGroup(self.graduations)

        self.indicator = SlipIndicator(parent=self)
        self.addToGroup(self.indicator)

        triangle = QGraphicsPolygonItem()
        self.addToGroup(triangle)

        polygon = QPolygonF([
            QPointF(0, -135),
            QPointF(width/2, -135-height),
            QPointF(-width/2, -135-height),
        ])
        
        triangle.setPolygon(polygon)
        triangle.setBrush(QBrush(Qt.GlobalColor.white))
        triangle.setPen(QPen(Qt.PenStyle.NoPen))

    def updatePositions(self, slip):
        self.indicator.updatePositions(slip)