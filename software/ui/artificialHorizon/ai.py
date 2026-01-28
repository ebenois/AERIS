from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsLineItem
from PyQt6.QtGui import QColor, QPen
from PyQt6.QtCore import Qt
import math

class DirectionAi(QGraphicsItemGroup):
    def __init__(self, parent=None):
        super().__init__(parent)
        width=70
        heigth=160

        line = QGraphicsLineItem(-width/2, 0 , width/2, 0, self)
        line.setPen(QPen(QColor("#FF00FF"), 3)) 

        line = QGraphicsLineItem(0, -heigth/2 , 0, heigth/2, self)
        line.setPen(QPen(QColor("#FF00FF"), 3))
    
    def updatePositions(self, pitch, roll, aimedPitch, aimedDirection):
        y=aimedPitch*math.cos(math.radians(roll))
        x=aimedPitch*math.sin(math.radians(roll))+aimedDirection
        self.setPos(x, y)