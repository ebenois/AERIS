from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsRectItem, QGraphicsLineItem
from PyQt6.QtGui import QPen, QBrush, QColor
from PyQt6.QtCore import Qt

from ui.artificialHorizon.graduations import PitchGraduations


class ArtificialHorizonBackground(QGraphicsItemGroup):
    def __init__(self, width, height):
        super().__init__()

        self.width = width
        self.height = height
        self.pixelsPerDegree = height / (2*22.5)
        self.cycleHeight = 360 * self.pixelsPerDegree
        blockHeight = 180 * self.pixelsPerDegree

        self.bg1 = self.CreateBlock(width, blockHeight)
        self.bg2 = self.CreateBlock(width, blockHeight)

        self.graduations = PitchGraduations(self, width, height)

    def CreateBlock(self, width, blockHeight):
        group = QGraphicsItemGroup(self)

        sky = QGraphicsRectItem(-width, -blockHeight, width * 2, blockHeight, group)
        sky.setBrush(QBrush(QColor("#0080FF")))
        sky.setPen(QPen(Qt.PenStyle.NoPen))

        ground = QGraphicsRectItem(-width, 0, width * 2, blockHeight, group)
        ground.setBrush(QBrush(QColor("#804000")))
        ground.setPen(QPen(Qt.PenStyle.NoPen))

        pen = QPen(QColor("white"), 5)

        for i in (-1, 0, 1):
            line = QGraphicsLineItem(-width, i * blockHeight, width * 2, i * blockHeight, group)
            line.setPen(pen)

        return group

    def updatePositions(self, pitch, roll):
        self.setRotation(-roll)

        y_offset = (pitch * self.pixelsPerDegree) % self.cycleHeight

        self.bg1.setPos(0, y_offset)
        self.bg2.setPos(0, y_offset - self.cycleHeight)

        self.graduations.updatePositions(pitch)