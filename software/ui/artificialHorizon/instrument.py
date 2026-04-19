from PyQt6.QtWidgets import (
    QGraphicsItemGroup,
    QGraphicsEllipseItem,
    QGraphicsLineItem,
    QGraphicsRectItem,
)
from PyQt6.QtGui import QPen, QColor, QBrush
from PyQt6.QtCore import Qt
import numbers

from ui.artificialHorizon.background import ArtificialHorizonBackground


class ArtificialHorizonInstrument(QGraphicsItemGroup):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.limit = 45

        self.isCritical = False
        self.isInError = True

        self.currentLineWeight = width // 30
        self.currentDotRadius = width // 30
        self.currentOutlineWeight = width // 75
        self.currentWingsDistance = width // 8
        self.currentWingsSpan = width // 4
        self.currentWingsHeight = width // 15

        # Initialisation du fond (Le masque est géré à l'intérieur)
        self.background = ArtificialHorizonBackground(width, height)
        self.addToGroup(self.background)
        self.background.setPos(0, 0) 

        self.alertFrame = QGraphicsRectItem(-width/2, -height/2, width, height)
        self.isInErrorPen = QPen(QColor("red"), 10)
        self.isCriticalPen = QPen(QColor("#ff7f00"), 10)
        self.alertFrame.setVisible(False)

        self.maquette = QGraphicsItemGroup()
        self.wings = []
        self.montants = []
        self.dots = []

        self.DrawIndicator("white", isOutline=True)
        self.DrawIndicator("black", isOutline=False)

        self.addToGroup(self.maquette)
        self.maquette.setPos(0, 0)
        self.maquette.setZValue(10)

        self.addToGroup(self.alertFrame)

    def CreatePen(self, color, isOutline):
        extra = self.currentOutlineWeight if isOutline else 0
        pen = QPen(QColor(color), self.currentLineWeight + extra)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        return pen

    def DrawIndicator(self, color, isOutline=False):
        pen = self.CreatePen(color, isOutline)

        for sign in (-1, 1):
            wing = QGraphicsLineItem()
            wing.setPen(pen)
            self.maquette.addToGroup(wing)
            self.wings.append((wing, isOutline, sign))

            montant = QGraphicsLineItem()
            montant.setPen(pen)
            self.maquette.addToGroup(montant)
            self.montants.append((montant, isOutline, sign))

        r = self.currentDotRadius + (self.currentOutlineWeight if isOutline else 0)
        dot = QGraphicsEllipseItem(-r / 2, -r / 2, r, r)
        dot.setBrush(QBrush(QColor(color)))
        dot.setPen(QPen(Qt.PenStyle.NoPen))
        self.maquette.addToGroup(dot)
        self.dots.append((dot, isOutline))

        self.UpdateWingsGeometry()

    def UpdateWingsGeometry(self):
        for wing, _, sign in self.wings:
            wing.setLine(
                sign * (self.currentWingsSpan + self.currentWingsDistance),
                0,
                sign * self.currentWingsDistance,
                0,
            )

        for montant, _, sign in self.montants:
            montant.setLine(
                sign * self.currentWingsDistance,
                0,
                sign * self.currentWingsDistance,
                self.currentWingsHeight,
            )

    def drawAlert(self, flashOpacity):
        if self.isInError:
            self.alertFrame.setPen(self.isInErrorPen)
            self.alertFrame.setVisible(True)
            self.alertFrame.setOpacity(flashOpacity)
            self.background.updatePositions("ERR", "ERR")
        elif self.isCritical:
            self.alertFrame.setPen(self.isCriticalPen)
            self.alertFrame.setVisible(True)
            self.alertFrame.setOpacity(0.4 + 0.6 * flashOpacity)
        else:
            self.alertFrame.setVisible(False)

    def drawLess(self, highMentalLoad):
        self.setOpacity(0.5 if highMentalLoad else 1.0)

    def updatePositions(self, pitch, roll):
        dataValid = isinstance(roll, numbers.Number) and isinstance(pitch, numbers.Number)

        if dataValid:
            self.isInError = False
            self.background.updatePositions(pitch, roll)
            if abs(pitch) >= self.limit or abs(roll) >= self.limit:
                self.isCritical = True
            else:
                self.isCritical = False
        else:
            self.isInError = True