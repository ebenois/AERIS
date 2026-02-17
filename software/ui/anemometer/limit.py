from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsRectItem
from PyQt6.QtGui import QBrush, QColor, QPen
from PyQt6.QtCore import Qt, QElapsedTimer

class SpeedLimit(QGraphicsItemGroup):
    def __init__(self, width, height):
        super().__init__()

        self.width = width
        self.height = height
        self.span = 60
        
        self.previousSpeed = None
        self.timer = QElapsedTimer()
        self.timer.start()

        self.rect = QGraphicsRectItem()
        self.rect.setBrush(QBrush(QColor("#FF0000")))
        self.rect.setPen(QPen(Qt.PenStyle.NoPen))
        self.addToGroup(self.rect)

    def updatePositions(self, speed):
        limit = 300        
        pixel_per_unit = (self.height / 2) / self.span
        height_in_pixels = (limit-speed) * pixel_per_unit

        safe_height = max(-self.height/2, min(self.height/2, height_in_pixels))
        
        self.rect.setRect(
            self.width * 15 / 17, 
            0,
            self.width *2/ 17, 
            self.height/2-safe_height
        )
        self.previousSpeed = speed