from PyQt6.QtWidgets import (
    QGraphicsItemGroup,
    QGraphicsLineItem,
    QGraphicsTextItem,
    QGraphicsRectItem,
    QGraphicsItem,
    QGraphicsPolygonItem,
)
from PyQt6.QtGui import QColor, QPen, QFont, QBrush, QPainterPath, QPolygonF
from PyQt6.QtCore import Qt, QRectF, QPointF
import numbers


class SpeedIndicator(QGraphicsItemGroup):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height

        self.knotsPerGraduation = 1
        self.pixelsPerGraduation = 40
        self.pxPerKnot = self.pixelsPerGraduation / self.knotsPerGraduation

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemClipsChildrenToShape, True)

        triangle = QGraphicsPolygonItem()
        self.addToGroup(triangle)

        polygon = QPolygonF(
            [
                QPointF(width * 5 / 7, -height / 15),
                QPointF(width * 6 / 7, 0),
                QPointF(width * 5 / 7, height / 15),
                QPointF(0, height / 15),
                QPointF(0, -height / 15),
            ]
        )

        triangle.setPolygon(polygon)
        triangle.setBrush(QBrush(Qt.GlobalColor.black))
        triangle.setPen(QPen(Qt.GlobalColor.white, 3))
        triangle.setPos(0, height / 2)

        self.font = QFont()
        self.font.setPixelSize(int(height / 16))

        self.digits = []
        for i in range(-2, 3):
            smallText = QGraphicsTextItem("", self)
            smallText.setDefaultTextColor(Qt.GlobalColor.white)
            smallText.setFont(self.font)
            variableText = QGraphicsTextItem("", self)
            variableText.setDefaultTextColor(Qt.GlobalColor.white)
            variableText.setFont(self.font)
            self.digits.append(
                {"index": i, "smallText": smallText, "variableText": variableText}
            )

    def updatePositions(self, speed):
        if not isinstance(speed, numbers.Number):
            for digit in self.digits:
                main = digit["smallText"]
                main.setPlainText(str(speed))
                rect = main.boundingRect()
                main.setPos(self.width / 20, self.height / 2 - rect.height() / 2)
                main.setVisible(True)
            return

        step = self.knotsPerGraduation * 2
        baseSpeed = (speed // step) * step
        centerY = self.height * 0.5

        tens = speed // 10

        for digit in self.digits:
            altVal = baseSpeed + digit["index"] * self.knotsPerGraduation
            yOffset = (speed - altVal) * self.pxPerKnot

            units = abs(altVal) % 10
            text = f"{units}"

            var = digit["variableText"]
            if var.toPlainText() != text:
                var.setPlainText(text)

            main = digit["smallText"]

            smallStr = f"{tens}"
            if main.toPlainText() != smallStr:
                main.setPlainText(smallStr)

            xVar = self.width / 20
            smallRect = main.boundingRect()
            main.setPos(xVar, centerY - smallRect.height() / 2)

            main.setVisible(True)

            rect = var.boundingRect()
            var.setPos(smallRect.width(), centerY + yOffset - rect.height() / 2)
            var.setVisible(True)

    def boundingRect(self):
        return QRectF(
            0, self.height / 2 - self.height / 15, self.width, self.height * 2 / 15
        )

    def shape(self):
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path
