from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsRectItem
from PyQt6.QtGui import QBrush, QColor, QPen
from PyQt6.QtCore import Qt, QElapsedTimer


class AltitudeLimit(QGraphicsItemGroup):
    def __init__(self, width, height, limit):
        super().__init__()

        self.limit = limit
        self.span = 500
        self.height = height
        self.pixelPerUnit = (self.height / 2) / self.span
        self.width = width

        self.timer = QElapsedTimer()
        self.timer.start()

        self.rect = QGraphicsRectItem()
        self.rect.setBrush(QBrush(QColor("#FF0000")))
        self.rect.setPen(QPen(Qt.PenStyle.NoPen))
        self.addToGroup(self.rect)

    def updatePositions(self, altitude):
        heightPx = (self.limit - altitude) * self.pixelPerUnit
        safe = max(-self.height / 2, min(self.height / 2, heightPx))
        self.rect.setRect(
            -self.width * 2 / 17, 0, self.width * 2 / 17, self.height / 2 - safe
        )
