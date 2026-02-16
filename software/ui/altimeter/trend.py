from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsRectItem
from PyQt6.QtGui import QBrush, QColor, QPen
from PyQt6.QtCore import Qt
import math

class AltitudeTrend(QGraphicsItemGroup):
    def __init__(self, width , height):
        super().__init__()

        self.width = width
        self.height = height

        self.rect = QGraphicsRectItem(
            0, self.height/2 ,
            self.width/17, 0
        )
        self.rect.setBrush(QBrush(QColor("#F6FF00")))
        self.rect.setPen(QPen(Qt.PenStyle.NoPen))
        self.addToGroup(self.rect)

    def updatePositions(self,speed,pitch):
        self.span = 500
        knotToFeet = 1.68781
        verticalSpeed =  speed * math.sin(math.radians(pitch)) * knotToFeet * 5 * (self.height/2)/self.span
        nextPosition = max(-self.height, min(self.height,verticalSpeed))
        self.rect.setRect(0, self.height/2 ,
            self.width/17, -nextPosition)
        return