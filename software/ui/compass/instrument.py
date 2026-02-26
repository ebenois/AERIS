from PyQt6.QtWidgets import (
    QGraphicsItemGroup,
    QGraphicsEllipseItem,
    QGraphicsPolygonItem,
)
from PyQt6.QtGui import QBrush, QColor, QPen, QPolygonF
from PyQt6.QtCore import Qt, QPointF

from ui.compass.graduations import DirectionGraduations


class CompassInstrument(QGraphicsItemGroup):
    def __init__(self, width, height):
        super().__init__()

        self.width = width
        self.height = height

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
        self.addToGroup(self.dot)

        self.graduations = DirectionGraduations(width)
        self.graduations.setPos(centerX, centerY)
        self.addToGroup(self.graduations)

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
        self.addToGroup(self.indicator)

        self.isInError = False

    def drawAlert(self, showRed):
        if showRed and self.isInError:
            self.dot.setPen(self.alertPen)
        else:
            self.dot.setPen(self.noPen)

    def updatePositions(self, heading):
        if isinstance(heading, (int, float)):
            self.isInError = False
            self.graduations.updatePositions(heading)
        else:
            self.isInError = True
