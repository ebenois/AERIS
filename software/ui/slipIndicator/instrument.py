from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsPolygonItem
from PyQt6.QtGui import QBrush, QPen, QPolygonF, QColor
from PyQt6.QtCore import Qt, QPointF
import numbers

from ui.slipIndicator.graduations import SlipGraduations
from ui.slipIndicator.indicator import SlipIndicator


class SlipInstrument(QGraphicsItemGroup):
    def __init__(self, width, height):
        super().__init__()

        polygonWidth = 25
        polygonHeight = 15
        self.limit = 30
        
        self.isInError = True
        self.isCritical = False

        self.graduations = SlipGraduations(width, height)
        self.addToGroup(self.graduations)

        self.indicator = SlipIndicator(width, height)
        self.addToGroup(self.indicator)

        self.triangle = QGraphicsPolygonItem()
        self.addToGroup(self.triangle)
        
        self.alertFrame = QGraphicsPolygonItem()
        self.addToGroup(self.alertFrame)

        polygon = QPolygonF(
            [
                QPointF(width / 2, width * 3 / (4 * 15)),
                QPointF(
                    width / 2 + polygonWidth / 2, width * 3 / (4 * 15) - polygonHeight
                ),
                QPointF(
                    width / 2 - polygonWidth / 2, width * 3 / (4 * 15) - polygonHeight
                ),
            ]
        )

        self.triangle.setPolygon(polygon)
        self.triangle.setBrush(QBrush(Qt.GlobalColor.white))
        self.alertFrame.setPolygon(polygon)
        self.triangle.setPen(QPen(QColor("#ff7f00")))
        
    def drawAlert(self, flashOpacity):
        if self.isInError:
            self.hide()            
        elif self.isCritical:
            self.show()  
            self.graduations.show()
            self.alertFrame.setVisible(True)
            self.alertFrame.setOpacity(0.4 + 0.7 * flashOpacity)
        else:
            self.show() 
            self.graduations.show()
            self.alertFrame.setVisible(False)
            
    def drawLess(self, highMentalLoad):
        if highMentalLoad:
            self.setOpacity(0.5)
        else:
            self.setOpacity(1)

    def updatePositions(self, slip):
        dataValid = isinstance(slip, numbers.Number)
        if dataValid:
            self.isInError = False
            self.indicator.updatePositions(slip)
            
            if abs(slip) >= self.limit:
                    self.isCritical = True
            else:
                self.isCritical = False
        else:
            self.isInError = True
