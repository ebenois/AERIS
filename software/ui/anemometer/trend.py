from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsRectItem
from PyQt6.QtGui import QBrush, QColor, QPen
from PyQt6.QtCore import Qt, QElapsedTimer


class SpeedTrend(QGraphicsItemGroup):
    def __init__(self, width, height):
        super().__init__()

        self.width = width
        self.height = height
        self.span = 70
        self.pixelPerUnit = (self.height / 2) / self.span

        self.previousSpeed = None
        self.timer = QElapsedTimer()
        self.timer.start()

        self.rect = QGraphicsRectItem()
        self.rect.setBrush(QBrush(QColor("#0080FF")))
        self.rect.setPen(QPen(Qt.PenStyle.NoPen))
        self.addToGroup(self.rect)

    def updatePositions(self, speed):
        dt = self.timer.elapsed() / 1000.0
        self.timer.restart()

        if self.previousSpeed is None or dt <= 0:
            self.previousSpeed = speed
            return

        acceleration = (speed - self.previousSpeed) / dt

        speedVariation = acceleration * 3

        heightPx = speedVariation * self.pixelPerUnit

        safe = max(-self.height / 2, min(self.height / 2, heightPx))

        self.rect.setRect(
            self.width * 15 / 17, self.height / 2, self.width * 2 / 17, -safe
        )
        self.previousSpeed = speed
