from PyQt6.QtWidgets import (
    QGraphicsItemGroup,
    QGraphicsEllipseItem,
    QGraphicsLineItem
)
from PyQt6.QtGui import QPen, QColor, QBrush
from PyQt6.QtCore import Qt

from ui.artificialHorizon.background import ArtificialHorizonBackground

class ArtificialHorizonInstrument(QGraphicsItemGroup):
    ecartMin, ecartMax, lineHeigth = 45, 120, 12
    
    def __init__(self):
        super().__init__()

        self.currentLineWeight = 10
        self.currentDotRadius = 10
        self.currentOutlineWeight = 5

        self.artificialHorizon = ArtificialHorizonBackground()
        self.addToGroup(self.artificialHorizon)

        self.maquette = QGraphicsItemGroup()
        self.addToGroup(self.maquette)

        self.lines = []
        self.dots = []

        self.drawIndicatorGeneric(color="white", isOutline=True)

        self.drawIndicatorGeneric(color="black", isOutline=False)

        center = self.boundingRect().center()
        self.setTransformOriginPoint(center)
        self.setPos(-center)

    def drawIndicatorGeneric(self, color, isOutline=False):
        if isOutline:
            extra = self.currentOutlineWeight
        else:
            extra = 0
        pen = QPen(QColor(color), self.currentLineWeight + extra)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        for sign in (-1, 1):
            # Ailes et Montants
            wing = QGraphicsLineItem(sign*self.ecartMax, 0, sign*self.ecartMin, 0)
            wing.setPen(pen)
            self.maquette.addToGroup(wing)
            self.lines.append((wing, isOutline))

            montant = QGraphicsLineItem(sign*self.ecartMin, 0, sign*self.ecartMin, self.lineHeigth)
            montant.setPen(pen)
            self.maquette.addToGroup(montant)
            self.lines.append((montant, isOutline))

        # Point central
        r = self.currentDotRadius + extra
        dot = QGraphicsEllipseItem(-r/2, -r/2, r, r)
        dot.setBrush(QBrush(QColor(color)))
        dot.setPen(QPen(Qt.PenStyle.NoPen))
        self.maquette.addToGroup(dot)
        self.dots.append((dot, isOutline))

    def setLineWeight(self, width):
        self.currentLineWeight = width
        for item, isOutline in self.lines:
            pen = item.pen()
            if isOutline:
                extra = self.currentOutlineWeight
            else:
                extra = 0
            pen.setWidth(self.currentLineWeight + extra)
            item.setPen(pen)

    def setDotSize(self, radius):
        self.currentDotRadius = radius
        for item, isOutline in self.dots:
            if isOutline:
                extra = self.currentOutlineWeight
            else:
                extra = 0
            r = self.currentDotRadius + extra
            item.setRect(-r/2, -r/2, r, r)

    def setOutlineWeight(self, weight):
        self.currentOutlineWeight = weight
        self.setLineWeight(self.currentLineWeight)
        self.setDotSize(self.currentDotRadius)
    
    def updatePositions(self, pitch, roll):
        self.artificialHorizon.updatePositions(pitch, roll)