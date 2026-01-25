from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsLineItem, QGraphicsTextItem, QGraphicsRectItem, QGraphicsItem, QGraphicsPolygonItem
from PyQt6.QtGui import QColor, QPen, QFont, QBrush, QPainterPath, QPolygonF
from PyQt6.QtCore import Qt, QRectF, QPointF
import math

class SpeedIndicator(QGraphicsItemGroup):
    def __init__(self, parent=None, width=60, height=50):
        super().__init__(parent)
        self.width = width
        self.height = height

        self.knotsPerGraduation = 1
        self.pixelsPerGraduation = 20
        self.pxPerKnot = self.pixelsPerGraduation / self.knotsPerGraduation

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemClipsChildrenToShape, True)

        triangle = QGraphicsPolygonItem()
        self.addToGroup(triangle)

        polygon = QPolygonF([
            QPointF(10, -25),
            QPointF(10, -15),
            QPointF(20, 0),
            QPointF(10, 15),
            QPointF(10, 25),
            QPointF(-35, 25),
            QPointF(-35, -25),
        ])

        triangle.setPolygon(polygon)
        triangle.setBrush(QBrush(Qt.GlobalColor.black))
        triangle.setPen(QPen(Qt.GlobalColor.white, 3))

        self.font = QFont("Arial", 18)

        self.digits = []
        for i in range(-1, 4):
            smallText = QGraphicsTextItem("", self)
            smallText.setDefaultTextColor(Qt.GlobalColor.white)
            smallText.setFont(self.font)
            variableText = QGraphicsTextItem("", self)
            variableText.setDefaultTextColor(Qt.GlobalColor.white)
            variableText.setFont(self.font)
            self.digits.append({
                "index": i,
                "smallText": smallText,
                "variableText": variableText
            })

    def updatePositions(self, speed):
        step = self.knotsPerGraduation * 2
        baseSpeed = (speed // step) * step

        mainDigit = self.digits[0]
        smallText = mainDigit["smallText"]

        tensDigit = speed // 10
        if speed<=0:
            smallText.setPlainText(f"-{abs(tensDigit):02d}")
            smallText.setPos(-45, -smallText.boundingRect().height() / 2)
        else:
            smallText.setPlainText(f"{tensDigit:02d}")
            smallText.setPos(-37, -smallText.boundingRect().height() / 2)
        smallText.setVisible(True)
    
        for numbers in self.digits:
            speedValue = baseSpeed + numbers["index"] * self.knotsPerGraduation
            y_local = (speed - speedValue) * self.pxPerKnot

            variableText = numbers["variableText"]
            unitsDigit = (speedValue % 10)
            variableText.setPlainText(str(unitsDigit))
            variableText.setPos(-10, y_local - variableText.boundingRect().height() / 2)
            variableText.setVisible(True)

    def boundingRect(self):
        return QRectF(-40, -26, 80, 52)

    def shape(self):
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path