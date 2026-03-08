from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsRectItem
from PyQt6.QtGui import QBrush, QColor, QPen
from PyQt6.QtCore import Qt
import numbers

from ui.variometer.graduations import RiseGraduations
from ui.variometer.indicator import RiseIndicator


class VariometerInstrument(QGraphicsItemGroup):
    def __init__(self, width, height):
        super().__init__()
        self.limit=50000
        self.width = width
        self.height = height
        
        self.isInError = True
        self.isCritical = False

        self.rect = QGraphicsRectItem(0, 0, self.width, self.height)

        self.rect.setBrush(QBrush(QColor("#808080")))
        self.rect.setPen(QPen(Qt.PenStyle.NoPen))
        self.addToGroup(self.rect)

        self.alertFrame = QGraphicsRectItem(0, 0, self.width, self.height)
        self.isInErrorPen = QPen(QColor("red"), 10)
        self.isCriticalPen = QPen(QColor("#ff7f00"), 10)
        self.alertFrame.setVisible(False)
        self.addToGroup(self.alertFrame)

        self.graduations = RiseGraduations(width, height)
        self.addToGroup(self.graduations)
        self.graduations.hide()

        self.indicator = RiseIndicator(width, height)
        self.addToGroup(self.indicator)
        self.indicator.setPos(width * 2 / 3, height / 2)

    def drawAlert(self, flashOn):
        if self.isInError:
            self.alertFrame.setPen(self.isInErrorPen)
            self.alertFrame.setVisible(flashOn)
            self.graduations.hide()
            
        elif self.isCritical:
            self.alertFrame.setPen(self.isCriticalPen)
            self.alertFrame.setVisible(flashOn)

        else:
            self.graduations.show()
            self.alertFrame.setVisible(False)
            
    def drawLess(self, highMentalLoad):
        if highMentalLoad:
            self.setOpacity(0.5)
        else:
            self.setOpacity(1)

    def updatePositions(self, climbRate):
        dataValid = isinstance(climbRate, numbers.Number)
        if dataValid:
            self.isInError = False
            self.indicator.updatePositions(climbRate)
            
            if abs(climbRate) >= self.limit:
                    self.isCritical = True
            else:
                self.isCritical = False
        else:
            self.isInError = True