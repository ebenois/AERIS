from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsLineItem
from PyQt6.QtGui import QColor, QPen
from PyQt6.QtCore import Qt
import math

class DirectionAi(QGraphicsItemGroup):
    def __init__(self, parent=None):
        super().__init__(parent)
        width=600
        heigth=600

        line = QGraphicsLineItem(-width/2, 0 , width/2, 0, self)
        line.setPen(QPen(QColor("#FF00FF"), 3)) 

        line = QGraphicsLineItem(0, -heigth , 0, heigth, self)
        line.setPen(QPen(QColor("#FF00FF"), 3))
    
    def updatePositions(self, pitch, roll, angle, aimedPitch, aimedAngle):
        y=(pitch-aimedPitch)*6.5
        maxOffeset = 60
        offset=aimedAngle-angle
        if offset>maxOffeset :
            offset=maxOffeset
        elif offset<-maxOffeset :
            offset=-maxOffeset
        x=math.sin(math.radians(offset))*223
        self.setPos(x, y)