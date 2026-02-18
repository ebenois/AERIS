from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsRectItem
from PyQt6.QtGui import QBrush, QColor, QPen
from PyQt6.QtCore import Qt, QElapsedTimer
import time

class SpeedTrend(QGraphicsItemGroup):
    def __init__(self, width, height):
        super().__init__()

        self.width = width
        self.height = height
        self.span = 70
        
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
        
        speed_variation_3s = acceleration * 3
        
        pixel_per_unit = (self.height / 2) / self.span
        height_in_pixels = speed_variation_3s * pixel_per_unit

        safe_height = max(-self.height/2, min(self.height/2, height_in_pixels))
        
        self.rect.setRect(
            self.width * 16 / 17, 
            self.height / 2,
            self.width / 17, 
            -safe_height
        )
        self.previousSpeed = speed