from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsRectItem
from PyQt6.QtGui import QBrush, QColor, QPen
from PyQt6.QtCore import Qt, QElapsedTimer


class SpeedLimit(QGraphicsItemGroup):
    def __init__(self, width, height):
        super().__init__()

        self.width = width
        self.height = height
        self.limit = 300
        self.span = 70
        self.pxPerKnot = self.height / (2 * self.span)

        self.timer = QElapsedTimer()
        self.timer.start()

        self.rect = QGraphicsRectItem()
        self.rect.setBrush(QBrush(QColor("#FF0000")))
        self.rect.setPen(QPen(Qt.PenStyle.NoPen))
        self.addToGroup(self.rect)

    def updatePositions(self, speed):
        heightPx = self.height / 2 - (self.limit - speed) * self.pxPerKnot
        safe = min(self.height, max(0, heightPx))
        self.rect.setRect(self.width, 0, self.width * 2 / 17, safe)
