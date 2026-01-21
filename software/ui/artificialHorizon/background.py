from PyQt6.QtWidgets import QGraphicsItem, QGraphicsItemGroup, QGraphicsRectItem, QGraphicsLineItem
from PyQt6.QtGui import QPen, QBrush, QColor
from PyQt6.QtCore import Qt
import math

from ui.artificialHorizon.graduations import PitchGraduations

class ArtificialHorizonBackground(QGraphicsItemGroup):
    def __init__(self):
        super().__init__()
        self.size = 310

        self.pitchItems = QGraphicsItemGroup(self)
        self.rollItems = QGraphicsItemGroup(self.pitchItems)

        width, height = self.size*2, self.size*2

        self.sky = QGraphicsRectItem(-width / 2, -height, width, height, self.rollItems)
        self.sky.setBrush(QBrush(QColor("#0080FF")))
        self.sky.setPen(QPen(Qt.PenStyle.NoPen))

        self.ground = QGraphicsRectItem(-width / 2, 0, width, height, self.rollItems)
        self.ground.setBrush(QBrush(QColor("#804000")))
        self.ground.setPen(QPen(Qt.PenStyle.NoPen))

        penHorizon = QPen(QColor("white"), 3)
        self.horizon = QGraphicsLineItem(-width / 2, 0, width / 2, 0, self.rollItems)
        self.horizon.setPen(penHorizon)

        self.graduations = PitchGraduations(parent=self,width_reference=width)

    def updatePositions(self, pitch, roll):
        pixelsPerDegree=6.5

        actualPitch = math.degrees(math.asin(math.sin(math.radians(pitch)) * math.cos(math.radians(roll))))

        horizonFlipped = False
        if actualPitch > 90:
            actualPitch = 180 - actualPitch
            horizonFlipped = True
        elif actualPitch < -90:
            actualPitch = -180 - actualPitch
            horizonFlipped = True
        
        self.rollItems.setRotation(-roll)

        if (roll > 90 and roll < 270) or (roll < -90 and roll > -270):
            offset = -actualPitch * pixelsPerDegree
        else:
            offset = actualPitch * pixelsPerDegree
            
        self.pitchItems.setPos(0, offset)

        self.graduations.updatePositions(offset, horizonFlipped, pixelsPerDegree)