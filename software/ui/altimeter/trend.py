from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsRectItem
from PyQt6.QtGui import QBrush, QColor, QPen
from PyQt6.QtCore import Qt
import math


class AltitudeTrend(QGraphicsItemGroup):
    def __init__(self, width, height):
        super().__init__()

        self.span = 500
        self.height = height
        self.knotToFeet = 1.68781
        self.size = (self.height / 2) / self.span
        self.width = width

        self.rect = QGraphicsRectItem(0, self.height / 2, self.width / 17, 0)
        self.rect.setBrush(QBrush(QColor("#0080FF")))
        self.rect.setPen(QPen(Qt.PenStyle.NoPen))
        self.addToGroup(self.rect)

    def updatePositions(self, speed, pitch):
        verticalSpeed = (
            speed * math.sin(math.radians(pitch)) * self.knotToFeet * 3 * self.size
        )
        snextPos = max(-self.height / 2, min(self.height / 2, verticalSpeed))
        self.rect.setRect(0, self.height / 2, self.width * 2 / 17, -snextPos)
