from PyQt6.QtWidgets import (
    QGraphicsItemGroup,
    QGraphicsEllipseItem,
    QGraphicsLineItem,
    QGraphicsRectItem,
)
from PyQt6.QtGui import QPen, QColor, QBrush, QPainterPath
from PyQt6.QtCore import Qt, QSettings, QRectF
import numbers

from ui.artificialHorizon.background import ArtificialHorizonBackground


class ArtificialHorizonInstrument(QGraphicsItemGroup):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height

        settings = QSettings("ENSC", "AERIS")

        self.currentLineWeight = settings.value("lineWeight", width // 30, int)
        self.currentDotRadius = settings.value("dotSize", width // 30, int)
        self.currentOutlineWeight = settings.value("outlineWeight", width // 75, int)
        self.currentWingsDistance = settings.value("WingsDistance", width // 8, int)
        self.currentWingsSpan = settings.value("WingsSpan", width // 4, int)
        self.currentWingsHeight = settings.value("WingsHeight", width // 15, int)

        self.setFlag(QGraphicsItemGroup.GraphicsItemFlag.ItemClipsChildrenToShape, True)

        self.background = ArtificialHorizonBackground(width, height)
        self.addToGroup(self.background)
        self.background.setPos(width / 2, height / 2)

        self.alertFrame = QGraphicsRectItem(0, 0, self.width, self.height)
        self.alertFrame.setPen(QPen(QColor("red"), 10))
        self.alertFrame.setVisible(False)
        self.addToGroup(self.alertFrame)

        self.isInError = True

        self.maquette = QGraphicsItemGroup()

        self.wings = []
        self.montants = []
        self.dots = []

        self.DrawIndicator("white", isOutline=True)
        self.DrawIndicator("black", isOutline=False)

        self.addToGroup(self.maquette)
        self.maquette.setPos(width / 2, height / 2)
        self.maquette.setZValue(10)

    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)

    def shape(self):
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path

    def CreatePen(self, color, isOutline):
        extra = self.currentOutlineWeight if isOutline else 0
        pen = QPen(QColor(color), self.currentLineWeight + extra)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        return pen

    def DrawIndicator(self, color, isOutline=False):
        pen = self.CreatePen(color, isOutline)

        for sign in (-1, 1):
            # Horizontal wing
            wing = QGraphicsLineItem()
            wing.setPen(pen)
            self.maquette.addToGroup(wing)
            self.wings.append((wing, isOutline, sign))

            # Vertical montant
            montant = QGraphicsLineItem()
            montant.setPen(pen)
            self.maquette.addToGroup(montant)
            self.montants.append((montant, isOutline, sign))

        # Center dot
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

    def setLineWeight(self, width):
        self.currentLineWeight = width
        for item_list in (self.wings, self.montants):
            for item, isOutline, _ in item_list:
                pen = item.pen()
                extra = self.currentOutlineWeight if isOutline else 0
                pen.setWidth(self.currentLineWeight + extra)
                item.setPen(pen)

    def setDotSize(self, radius):
        self.currentDotRadius = radius
        for dot, isOutline in self.dots:
            extra = self.currentOutlineWeight if isOutline else 0
            r = self.currentDotRadius + extra
            dot.setRect(-r / 2, -r / 2, r, r)

    def setOutlineWeight(self, weight):
        self.currentOutlineWeight = weight
        self.setLineWeight(self.currentLineWeight)
        self.setDotSize(self.currentDotRadius)

    def setWingsDistance(self, value):
        self.currentWingsDistance = value
        self.UpdateWingsGeometry()

    def setWingsSpan(self, value):
        self.currentWingsSpan = value
        self.UpdateWingsGeometry()

    def setWingsHeight(self, value):
        self.currentWingsHeight = value
        self.UpdateWingsGeometry()

    def drawAlert(self, flashOn):
        if self.isInError:
            self.alertFrame.setVisible(flashOn)
            self.background.updatePositions("ERR", "ERR")
        else:
            self.alertFrame.setVisible(False)

    def updatePositions(self, roll, pitch):
        dataValid = isinstance(roll, numbers.Number) and isinstance(
            pitch, numbers.Number
        )

        if dataValid:
            self.isInError = False
            self.background.updatePositions(pitch, roll)
        else:
            self.isInError = True
