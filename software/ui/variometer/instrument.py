from PyQt6.QtWidgets import (
    QGraphicsItemGroup,
    QGraphicsRectItem,
    QGraphicsItem,
    QGraphicsLineItem,
)
from PyQt6.QtGui import QBrush, QColor, QPen
from PyQt6.QtCore import Qt
import numbers

from ui.variometer.graduations import RiseGraduations
from ui.variometer.indicator import RiseIndicator


class VariometerInstrument(QGraphicsItemGroup):
    def __init__(self, width, height):
        super().__init__()

        self.width = width
        self.height = height

        self.rect = QGraphicsRectItem(0, 0, self.width, self.height)

        self.rect.setBrush(QBrush(QColor("#808080")))
        self.rect.setPen(QPen(Qt.PenStyle.NoPen))
        self.addToGroup(self.rect)

        self.noDataEffect = QPen(Qt.PenStyle.NoPen)
        self.rect.setPen(self.noDataEffect)

        self.graduations = RiseGraduations(width, height)
        self.addToGroup(self.graduations)
        self.graduations.hide()

        self.indicator = RiseIndicator(width, height)
        self.addToGroup(self.indicator)
        self.indicator.setPos(width * 2 / 3, height / 2)

        self.isInError = False

    def drawAlert(self, showRed):
        if showRed and self.isInError:
            self.rect.setPen(QPen(QColor("red"), 10))
        else:
            self.rect.setPen(QPen(Qt.PenStyle.NoPen))

    def updatePositions(self, climbRate):
        if isinstance(climbRate, numbers.Number):
            self.isInError = False
            self.indicator.updatePositions(climbRate)
            self.graduations.show()
        else:
            self.isInError = True
            self.graduations.hide()
