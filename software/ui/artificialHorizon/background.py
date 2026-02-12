from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsRectItem, QGraphicsLineItem, QGraphicsEllipseItem
from PyQt6.QtGui import QPen, QBrush, QColor
from PyQt6.QtCore import Qt
import math

from ui.artificialHorizon.graduations import PitchGraduations

class ArtificialHorizonBackground(QGraphicsItemGroup):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.pixelsPerDegree = height/(2*22.5)
        
        self.movingItems = QGraphicsItemGroup(self)
        
        self.cycleHeight = 360 * self.pixelsPerDegree 

        blockH = 180 * self.pixelsPerDegree 

        self.bg1 = QGraphicsItemGroup(self.movingItems)
        self.bg2 = QGraphicsItemGroup(self.movingItems)

        for group in [self.bg1, self.bg2]:
            sky = QGraphicsRectItem(-width, -blockH, width*2, blockH, group)
            sky.setBrush(QBrush(QColor("#0080FF")))
            sky.setPen(QPen(Qt.PenStyle.NoPen))
            
            ground = QGraphicsRectItem(-width, 0, width*2, blockH, group)
            ground.setBrush(QBrush(QColor("#804000")))
            ground.setPen(QPen(Qt.PenStyle.NoPen))

            for i in [-1,0,1]:
                line = QGraphicsLineItem(-width, i*blockH , width*2, i*blockH, group)
                line.setPen(QPen(QColor("white"), 3))

        self.graduations = PitchGraduations(self.movingItems, width, height)

    def updatePositions(self, pitch, roll):
        self.movingItems.setRotation(-roll)

        y_offset = (pitch * self.pixelsPerDegree) % self.cycleHeight
        
        self.bg1.setPos(0, y_offset)
        self.bg2.setPos(0, y_offset - self.cycleHeight)

        self.graduations.updatePositions(pitch)