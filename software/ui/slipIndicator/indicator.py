from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsPolygonItem
from PyQt6.QtGui import QPen, QBrush, QPolygonF
from PyQt6.QtCore import Qt, QPointF
import math


class SlipIndicator(QGraphicsItemGroup):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.radius = height

        polygonWidth = 30
        polygonHeight = 15

        triangle = QGraphicsPolygonItem()
        self.addToGroup(triangle)

        polygon = QPolygonF(
            [
                QPointF(0, -self.radius + width * 3 / (4 * 15)),
                QPointF(
                    polygonWidth / 2,
                    -self.radius + polygonHeight + width * 3 / (4 * 15),
                ),
                QPointF(
                    -polygonWidth / 2,
                    -self.radius + polygonHeight + width * 3 / (4 * 15),
                ),
            ]
        )

        triangle.setPolygon(polygon)
        triangle.setBrush(QBrush(Qt.GlobalColor.white))
        triangle.setPen(QPen(Qt.PenStyle.NoPen))
        self.setTransformOriginPoint(width / 2, self.radius)
        triangle.setPos(width / 2, self.radius)

    def updatePositions(self, slip):
        maxRotation = 60
        pixels = max(-maxRotation, min(maxRotation, slip*60))

        self.setRotation(pixels * math.tanh(self.width / (2 * self.radius)))
