from PyQt6.QtWidgets import (
    QGraphicsItemGroup,
    QGraphicsRectItem,
    QGraphicsLineItem,
)
from PyQt6.QtGui import QPen, QBrush, QColor
from PyQt6.QtCore import Qt

from ui.artificialHorizon.graduations import PitchGraduations


class ArtificialHorizonBackground(QGraphicsItemGroup):
    def __init__(self, width, height):
        super().__init__()

        self.width = width
        self.height = height

        self.pixelsPerDegree = height / 45.0
        self.cycleHeight = 360.0 * self.pixelsPerDegree
        self.blockHeight = 180.0 * self.pixelsPerDegree

        self.noPen = QPen(Qt.PenStyle.NoPen)
        self.skyBrush = QBrush(QColor("#0080FF"))
        self.groundBrush = QBrush(QColor("#804000"))
        self.horizonPen = QPen(QColor("white"), 5)

        self.bg1 = self.CreateBlock()
        self.bg2 = self.CreateBlock()

        self.graduations = PitchGraduations(self, width, height)

    def CreateBlock(self):
        group = QGraphicsItemGroup(self)

        width = self.width
        height = self.blockHeight

        sky = QGraphicsRectItem(-width, -height, width * 2, height, group)
        sky.setBrush(self.skyBrush)
        sky.setPen(self.noPen)

        ground = QGraphicsRectItem(-width, 0, width * 2, height, group)
        ground.setBrush(self.groundBrush)
        ground.setPen(self.noPen)

        for i in (-1, 0, 1):
            line = QGraphicsLineItem(-width, i * height, width * 2, i * height, group)
            line.setPen(self.horizonPen)

        return group

    def updatePositions(self, pitch, roll):
        self.setRotation(-roll)

        pixelsPerDegree = self.pixelsPerDegree
        cycleHeight = self.cycleHeight

        yOffset = (pitch * pixelsPerDegree) % cycleHeight

        self.bg1.setPos(0, yOffset)
        self.bg2.setPos(0, yOffset - cycleHeight)

        self.graduations.updatePositions(pitch)
