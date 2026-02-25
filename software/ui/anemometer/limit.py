from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsRectItem
from PyQt6.QtGui import QBrush, QColor, QPen
from PyQt6.QtCore import Qt, QElapsedTimer


class SpeedLimit(QGraphicsItemGroup):
    def __init__(self, width, height):
        super().__init__()

        self.width = width
        self.height = height
        self.span = 60
        self.limit = 300
        self.pixelPerUnit = (self.height / 2) / self.span

        self.timer = QElapsedTimer()
        self.timer.start()

        self.rect = QGraphicsRectItem()
        self.rect.setBrush(QBrush(QColor("#FF0000")))
        self.rect.setPen(QPen(Qt.PenStyle.NoPen))
        self.addToGroup(self.rect)

    def updatePositions(self, speed):
        heightPx = (self.limit - speed) * self.pixelPerUnit
        safe = max(-self.height / 2, min(self.height / 2, heightPx))
        self.rect.setRect(self.width, 0, self.width * 2 / 17, self.height / 2 - safe)
