from PyQt6.QtWidgets import (
    QGraphicsItemGroup,
    QGraphicsEllipseItem,
    QGraphicsLineItem,
    QGraphicsItem
)
from PyQt6.QtGui import QPen, QColor, QBrush, QPainterPath
from PyQt6.QtCore import Qt, QSettings, QRectF

from ui.artificialHorizon.background import ArtificialHorizonBackground

class ArtificialHorizonInstrument(QGraphicsItemGroup):  
    def __init__(self):
        super().__init__()

        settings = QSettings("ENSC", "AERIS")
        self.size = 310
        self.currentLineWeight = settings.value("lineWeight", 10, int)
        self.currentDotRadius = settings.value("dotSize", 10, int)
        self.currentOutlineWeight = settings.value("outlineWeight", 5, int)
        self.currentWingsDistance = settings.value("WingsDistance", 45, int)
        self.currentWingsSpan = settings.value("WingsSpan", 75, int)
        self.currentWingsHeight = settings.value("WingsHeight", 12, int)

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemClipsChildrenToShape, True)

        self.artificialHorizon = ArtificialHorizonBackground()
        self.addToGroup(self.artificialHorizon)

        self.maquette = QGraphicsItemGroup()
        self.addToGroup(self.maquette)
        self.maquette.setZValue(10)

        self.lines = []
        self.dots = []
        self.drawIndicatorGeneric(color="white", isOutline=True)
        self.drawIndicatorGeneric(color="black", isOutline=False)

        center = self.boundingRect().center()
        self.setTransformOriginPoint(center)
        self.setPos(-center)

    def boundingRect(self):
        return QRectF(-self.size / 2, -self.size / 2, self.size, self.size)

    def shape(self):
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path

    def drawIndicatorGeneric(self, color, isOutline=False):
        if isOutline:
            extra = self.currentOutlineWeight
        else:
            extra = 0
        pen = QPen(QColor(color), self.currentLineWeight + extra)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        for sign in (-1, 1):
            # Ailes et Montants
            wing = QGraphicsLineItem(sign*(self.currentWingsSpan+self.currentWingsDistance), 0, sign*self.currentWingsDistance, 0)
            wing.setPen(pen)
            self.maquette.addToGroup(wing)
            self.lines.append((wing, isOutline))

            montant = QGraphicsLineItem(sign*self.currentWingsDistance, 0, sign*self.currentWingsDistance, self.currentWingsHeight)
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
    
    def setWingsDistance(self, width):
        self.currentWingsDistance = width
        for item, isOutline in self.lines:
            currentLine = item.line()
            if currentLine.x1() < 0:
                sign = -1 
            else:
                sign = 1
            if currentLine.y1() == currentLine.y2():
                item.setLine(
                    sign * (self.currentWingsSpan + self.currentWingsDistance), 0, 
                    sign * self.currentWingsDistance, 0
                )
            else:
                item.setLine(
                    sign * self.currentWingsDistance, 0, 
                    sign * self.currentWingsDistance, self.currentWingsHeight
                )

    def setWingsSpan(self, span):
        self.currentWingsSpan = span
        for item, isOutline in self.lines:
            currentLine = item.line()
            if currentLine.x1() < 0:
                sign = -1 
            else:
                sign = 1
            if currentLine.y1() == currentLine.y2():
                item.setLine(
                    sign * (self.currentWingsSpan + self.currentWingsDistance), 0, 
                    sign * self.currentWingsDistance, 0
                )
            else:
                item.setLine(
                    sign * self.currentWingsDistance, 0, 
                    sign * self.currentWingsDistance, self.currentWingsHeight
                )
    
    def setWingsHeight(self, height):
        self.currentWingsHeight = height
        for item, isOutline in self.lines:
            currentLine = item.line()
            if currentLine.x1() < 0:
                sign = -1 
            else:
                sign = 1
            if currentLine.y1() == currentLine.y2():
                item.setLine(
                    sign * (self.currentWingsSpan + self.currentWingsDistance), 0, 
                    sign * self.currentWingsDistance, 0
                )
            else:
                item.setLine(
                    sign * self.currentWingsDistance, 0, 
                    sign * self.currentWingsDistance, self.currentWingsHeight
                )
    
    def updatePositions(self, pitch, roll, angle):
        self.artificialHorizon.updatePositions(pitch, roll, angle)