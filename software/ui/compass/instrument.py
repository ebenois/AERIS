from PyQt6.QtWidgets import (
    QGraphicsItemGroup,
    QGraphicsEllipseItem,
    QGraphicsPolygonItem,
)
from PyQt6.QtGui import QBrush, QColor, QPen, QPolygonF
from PyQt6.QtCore import Qt, QPointF
import numbers

from ui.compass.graduations import DirectionGraduations


class CompassInstrument(QGraphicsItemGroup):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        
        self.isCritical = False

        centerX = width / 2
        centerY = height / 2

        self.noPen = QPen(Qt.PenStyle.NoPen)
        self.alertPen = QPen(QColor("red"), 15)
        self.bgBrush = QBrush(QColor("#808080"))
        self.indicatorBrush = QBrush(Qt.GlobalColor.black)
        self.indicatorPen = QPen(Qt.GlobalColor.white, 3)

        self.dot = QGraphicsEllipseItem(0, 0, width, height)
        self.dot.setBrush(self.bgBrush)
        self.dot.setPen(self.noPen)

        self.graduations = DirectionGraduations(width)
        self.graduations.setPos(centerX, centerY)

        polygonWidth = 55
        polygonHeight = 45

        polygon = QPolygonF(
            [
                QPointF(centerX, 0),
                QPointF(centerX + polygonWidth / 2, -polygonHeight),
                QPointF(centerX - polygonWidth / 2, -polygonHeight),
            ]
        )

        self.indicator = QGraphicsPolygonItem(polygon)
        self.indicator.setBrush(self.indicatorBrush)
        self.indicator.setPen(self.indicatorPen)

        for item in [self.dot, self.graduations, self.indicator]:
            self.addToGroup(item)

        self.isInError = True

    def drawAlert(self, flashOn):
        if self.isInError:
            self.dot.setPen(self.alertPen if flashOn else self.noPen)
            self.graduations.hide()
        else:
            self.dot.setPen(self.noPen)
            self.graduations.show()
            
    def drawLess(self, highMentalLoad):
        if highMentalLoad:
            self.setOpacity(0.5)
        else:
            self.setOpacity(1)

    def updatePositions(self, heading):
        dataValid = isinstance(heading, numbers.Number)

        if dataValid:
            self.isInError = False
            self.graduations.updatePositions(heading)
        else:
            self.isInError = True
