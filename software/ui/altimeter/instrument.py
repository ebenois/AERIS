from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsRectItem, QGraphicsItem
from PyQt6.QtGui import QBrush, QColor, QPen, QPainterPath
from PyQt6.QtCore import Qt, QRectF
import numbers

from ui.altimeter.graduations import AltitudeGraduations
from ui.altimeter.indicator import AltitudeIndicator
from ui.altimeter.trend import AltitudeTrend

class AltimeterInstrument(QGraphicsItemGroup):
    def __init__(self, width , height):
        super().__init__()
        self.width = width
        self.heigth = height

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemClipsChildrenToShape, True)

        self.rect = QGraphicsRectItem(
            0, 0,
            self.width, self.heigth
        )
        
        self.rect.setBrush(QBrush(QColor("#808080")))
        self.rect.setPen(QPen(Qt.PenStyle.NoPen))
        self.addToGroup(self.rect)

        self.noDataEffect = QPen(Qt.PenStyle.NoPen)
        self.rect.setPen(self.noDataEffect)

        self.graduations = AltitudeGraduations(width, height)
        self.addToGroup(self.graduations)

        self.indicator = AltitudeIndicator(width, height)
        self.addToGroup(self.indicator)

        self.trend = AltitudeTrend(width,height)
        self.addToGroup(self.trend)

        self.isInError = False 

    def drawAlert(self, showRed):
        if showRed and self.isInError:
            self.rect.setPen(QPen(QColor("red"), 15))
        else:
            self.rect.setPen(QPen(Qt.PenStyle.NoPen))

    def updatePositions(self, data):
        altitude = 38000
        speed = 280
        roll, pitch = data
        if isinstance(altitude, numbers.Number):
            self.isInError = False
            self.graduations.updatePositions(altitude)
            self.indicator.updatePositions(altitude)
            if isinstance(speed, numbers.Number) and isinstance(pitch, numbers.Number):
                self.trend.updatePositions(speed,pitch)
        else:
            self.isInError = True
            self.indicator.updatePositions("Error")

    def boundingRect(self):
        return QRectF(0, 0, self.width*2, self.heigth)

    def shape(self):
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path