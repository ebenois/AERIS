from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsLineItem, QGraphicsTextItem, QGraphicsRectItem, QGraphicsItem, QGraphicsPolygonItem
from PyQt6.QtGui import QColor, QPen, QFont, QBrush, QPainterPath, QPolygonF
from PyQt6.QtCore import Qt, QRectF, QPointF
import math


class AltitudeIndicator(QGraphicsItemGroup):
    def __init__(self, parent=None, width=60, height=50):
        super().__init__(parent)
        self.width = width
        self.height = height

        self.metersPerGraduation = 20
        self.pixelsPerGraduation = 18
        self.pxPerMeter = self.pixelsPerGraduation / self.metersPerGraduation

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemClipsChildrenToShape, True)

        triangle = QGraphicsPolygonItem()
        self.addToGroup(triangle)

        polygon = QPolygonF([
            QPointF(-10, -25),
            QPointF(-10, -15),
            QPointF(-20, 0),
            QPointF(-10, 15),
            QPointF(-10, 25),
            QPointF(50, 25),
            QPointF(50, -25),
        ])

        triangle.setPolygon(polygon)
        triangle.setBrush(QBrush(Qt.GlobalColor.black))
        triangle.setPen(QPen(Qt.GlobalColor.white, 3))

        self.bigFont = QFont("Arial", 18)
        self.smallFont = QFont("Arial", 14)

        self.digits = []
        for i in range(-1, 4):
            bigText = QGraphicsTextItem("", self)
            bigText.setDefaultTextColor(Qt.GlobalColor.white)
            bigText.setFont(self.bigFont)
            smallText = QGraphicsTextItem("", self)
            smallText.setDefaultTextColor(Qt.GlobalColor.white)
            smallText.setFont(self.smallFont)
            variableText = QGraphicsTextItem("", self)
            variableText.setDefaultTextColor(Qt.GlobalColor.white)
            variableText.setFont(self.smallFont)
            self.digits.append({
                "index": i,
                "bigText": bigText,
                "smallText": smallText,
                "variableText": variableText
            })

    def updatePositions(self, altitude):
        step = self.metersPerGraduation * 2
        baseAltitude = (altitude // step) * step

        mainDigit = self.digits[0]
        bigText = mainDigit["bigText"]
        smallText = mainDigit["smallText"]

        thousandsDigit = abs(altitude)//1000
        if altitude>=0:
            bigText.setPlainText(f"{thousandsDigit:02d}")
            bigText.setPos(-12, -bigText.boundingRect().height() / 2)
        else:
            bigText.setPlainText(f"-{thousandsDigit:02d}")
            bigText.setPos(-20, -bigText.boundingRect().height() / 2)
        bigText.setVisible(True)

        hundredsDigit = (altitude % 1000) // 100
        smallText.setPlainText(str(hundredsDigit))
        smallText.setPos(15, -smallText.boundingRect().height() / 2)
        smallText.setVisible(True)
    
        for numbers in self.digits:
            altitudeValue = baseAltitude + numbers["index"] * self.metersPerGraduation
            y_local = (altitude - altitudeValue) * self.pxPerMeter

            variableText = numbers["variableText"]
            tensDigit = (altitudeValue % 100) // 10 * 10
            variableText.setPlainText(f"{tensDigit:02d}")
            variableText.setPos(25, y_local - variableText.boundingRect().height() / 2)
            variableText.setVisible(True)

    def boundingRect(self):
        return QRectF(-20, -26, 80, 52)

    def shape(self):
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path