from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsRectItem
from PyQt6.QtGui import QBrush, QColor, QPen
from PyQt6.QtCore import Qt
import numbers

from ui.anemometer.graduations import SpeedGraduations
from ui.anemometer.indicator import SpeedIndicator
from ui.anemometer.trend import SpeedTrend
from ui.anemometer.limit import SpeedLimit


class AnemometerInstrument(QGraphicsItemGroup):
    def __init__(self, width, height):
        super().__init__()
        self.height = height
        self.width = width
        self.limitmin = 180
        self.limitmax = 300

        self.isInError = True
        self.isCritical = False

        self.rect = QGraphicsRectItem(0, 0, width, height)
        self.rect.setBrush(QBrush(QColor("#808080")))
        self.rect.setPen(QPen(Qt.PenStyle.NoPen))

        self.alertFrame = QGraphicsRectItem(0, 0, self.width, self.height)
        self.isInErrorPen = QPen(QColor("red"), 10)
        self.isCriticalPen = QPen(QColor("#ff7f00"), 10)
        self.alertFrame.setVisible(False)

        self.limit = SpeedLimit(width, height, self.limitmax)
        self.trend = SpeedTrend(width, height)
        self.graduations = SpeedGraduations(width, height)
        self.indicator = SpeedIndicator(width, height)

        for item in [
            self.rect,
            self.limit,
            self.trend,
            self.graduations,
            self.indicator,
            self.alertFrame,
        ]:
            self.addToGroup(item)

    def drawAlert(self, flashOpacity):
        if self.isInError:
            self.alertFrame.setPen(self.isInErrorPen)
            self.alertFrame.setVisible(True)
            self.alertFrame.setOpacity(flashOpacity)

            self.graduations.hide()
            self.trend.hide()
            self.limit.hide()
            self.indicator.updatePositions("ERR")

        elif self.isCritical:
            self.alertFrame.setPen(self.isCriticalPen)
            self.alertFrame.setVisible(True)
            self.alertFrame.setOpacity(0.4 + 0.6 * flashOpacity)

        else:
            self.graduations.show()
            self.trend.show()
            self.limit.show()
            self.alertFrame.setVisible(False)

    def drawLess(self, highMentalLoad):
        if highMentalLoad:
            self.setOpacity(0.5)
        else:
            self.setOpacity(1)

    def updatePositions(self, windSpeed):
        dataValid = isinstance(windSpeed, numbers.Number)

        if dataValid:
            self.isInError = False

            self.graduations.updatePositions(windSpeed)
            self.indicator.updatePositions(windSpeed)
            self.limit.updatePositions(windSpeed)
            self.trend.updatePositions(windSpeed)

            if windSpeed <= self.limitmin or windSpeed >= self.limitmax:
                self.isCritical = True
            else:
                self.isCritical = False

        else:
            self.isInError = True
