from PyQt6.QtWidgets import (
    QGraphicsItemGroup,
    QGraphicsRectItem,
    QGraphicsLineItem,
)
from PyQt6.QtGui import QPen, QBrush, QColor, QPainterPath
from PyQt6.QtCore import Qt, QRectF
import numbers

from ui.artificialHorizon.graduations import PitchGraduations


class ArtificialHorizonBackground(QGraphicsItemGroup):
    def __init__(self, width, height):
        super().__init__()

        self.width = width
        self.height = height

        self.pixelsPerDegree = height / 45.0
        self.cycleHeight = 360.0 * self.pixelsPerDegree
        self.blockHeight = 180.0 * self.pixelsPerDegree

        # Ce groupe (self) est le MASQUE. Il ne doit JAMAIS tourner.
        self.setFlag(QGraphicsItemGroup.GraphicsItemFlag.ItemClipsChildrenToShape, True)

        self.movingContent = QGraphicsItemGroup(self)

        self.noPen = QPen(Qt.PenStyle.NoPen)
        self.skyBrush = QBrush(QColor("#0080FF"))
        self.groundBrush = QBrush(QColor("#804000"))
        self.horizonPen = QPen(QColor("white"), 5)

        # On ajoute les blocs au groupe mobile
        self.bg1 = self.CreateBlock()
        self.bg2 = self.CreateBlock()
        self.movingContent.addToGroup(self.bg1)
        self.movingContent.addToGroup(self.bg2)

        self.graduations = PitchGraduations(self.movingContent, width, height)

    def CreateBlock(self):
        group = QGraphicsItemGroup()

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
        if not isinstance(roll, numbers.Number) or not isinstance(pitch, numbers.Number):
            self.movingContent.setRotation(0)
            self.bg1.setPos(0, 0)
            self.bg2.setPos(0, 0)
            self.graduations.hide()
            return

        self.movingContent.setRotation(-roll)

        pixelsPerDegree = self.pixelsPerDegree
        cycleHeight = self.cycleHeight

        # Le décalage vertical (Pitch)
        yOffset = (pitch * pixelsPerDegree) % cycleHeight

        self.bg1.setPos(0, yOffset)
        self.bg2.setPos(0, yOffset - cycleHeight)

        self.graduations.updatePositions(pitch)
        self.graduations.show()

    def boundingRect(self):
        # C'est cette zone qui définit le "carré" de ton instrument
        return QRectF(-self.width / 2, -self.height / 2, self.width, self.height)

    def shape(self):
        # Le masque de découpe suit exactement le boundingRect
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path