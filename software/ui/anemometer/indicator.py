from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsLineItem, QGraphicsTextItem, QGraphicsRectItem, QGraphicsItem, QGraphicsPolygonItem
from PyQt6.QtGui import QColor, QPen, QFont, QBrush, QPainterPath, QPolygonF
from PyQt6.QtCore import Qt, QRectF, QPointF
import math

class SpeedIndicator(QGraphicsItemGroup):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height

        self.knotsPerGraduation = 1
        self.pixelsPerGraduation = height/20
        self.pxPerKnot = self.pixelsPerGraduation / self.knotsPerGraduation

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemClipsChildrenToShape, True)

        triangle = QGraphicsPolygonItem()
        self.addToGroup(triangle)

        polygon = QPolygonF([
            QPointF(width*5/7, -height/15),
            QPointF(width*6/7, 0),
            QPointF(width*5/7, height/15),
            QPointF(0, height/15),
            QPointF(0, -height/15),
        ])

        triangle.setPolygon(polygon)
        triangle.setBrush(QBrush(Qt.GlobalColor.black))
        triangle.setPen(QPen(Qt.GlobalColor.white, 3))
        triangle.setPos(0,height/2)

        self.font = QFont("Arial", int(height/21))

        self.digits = []
        for i in range(-2, 3):
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
            smallText.setPos(self.width/30, self.height/2-smallText.boundingRect().height() / 2)
        else:
            smallText.setPlainText(f"{tensDigit:02d}")
            smallText.setPos(self.width/20, self.height/2-smallText.boundingRect().height() / 2)
        smallText.setVisible(True)
    
        for numbers in self.digits:
            speedValue = baseSpeed + numbers["index"] * self.knotsPerGraduation
            y_local = (speed - speedValue) * self.pxPerKnot

            if (speed < 0):
                y_local = -y_local

            variableText = numbers["variableText"]
            unitsDigit = (speedValue % 10)
            variableText.setPlainText(str(unitsDigit))
            variableText.setPos(smallText.boundingRect().width(), self.height/2 + y_local - variableText.boundingRect().height() / 2)
            variableText.setVisible(True)

    def boundingRect(self):
        return QRectF(0, self.height/2-self.height/15, self.width, self.height*2/15)

    def shape(self):
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path