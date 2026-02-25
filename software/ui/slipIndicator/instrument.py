from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsPolygonItem
from PyQt6.QtGui import QBrush, QPen, QPolygonF
from PyQt6.QtCore import Qt, QPointF
import numbers

from ui.slipIndicator.graduations import SlipGraduations
from ui.slipIndicator.indicator import SlipIndicator


class SlipInstrument(QGraphicsItemGroup):
    def __init__(self, width, height):
        super().__init__()

        polygonWidth = 25
        polygonHeight = 15

        self.graduations = SlipGraduations(width, height)
        self.addToGroup(self.graduations)

        self.indicator = SlipIndicator(width, height)
        self.addToGroup(self.indicator)

        triangle = QGraphicsPolygonItem()
        self.addToGroup(triangle)

        polygon = QPolygonF(
            [
                QPointF(width / 2, width * 3 / (4 * 15)),
                QPointF(
                    width / 2 + polygonWidth / 2, width * 3 / (4 * 15) - polygonHeight
                ),
                QPointF(
                    width / 2 - polygonWidth / 2, width * 3 / (4 * 15) - polygonHeight
                ),
            ]
        )

        triangle.setPolygon(polygon)
        triangle.setBrush(QBrush(Qt.GlobalColor.white))
        triangle.setPen(QPen(Qt.PenStyle.NoPen))

        self.hide()

    def updatePositions(self, data):
        packetId,roll,pitch,altitude,climbRate,windSpeed,heading,slip,button = data
        if isinstance(slip, numbers.Number):
            self.indicator.updatePositions(slip)
            self.show()
        else:
            self.hide()
