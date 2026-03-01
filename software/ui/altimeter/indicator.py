from PyQt6.QtWidgets import (
    QGraphicsItemGroup,
    QGraphicsTextItem,
    QGraphicsItem,
    QGraphicsPolygonItem,
)
from PyQt6.QtGui import QPen, QFont, QBrush, QPainterPath, QPolygonF
from PyQt6.QtCore import Qt, QRectF, QPointF
import numbers


class AltitudeIndicator(QGraphicsItemGroup):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height

        self.metersPerGraduation = 20
        self.pixelsPerGraduation = 40
        self.pxPerMeter = self.pixelsPerGraduation / self.metersPerGraduation

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemClipsChildrenToShape, True)

        triangle = QGraphicsPolygonItem()
        self.addToGroup(triangle)

        polygon = QPolygonF(
            [
                QPointF(0, -height / 15),
                QPointF(-width / 7, 0),
                QPointF(0, height / 15),
                QPointF(width, height / 15),
                QPointF(width, -height / 15),
            ]
        )

        triangle.setPolygon(polygon)
        triangle.setBrush(QBrush(Qt.GlobalColor.black))
        triangle.setPen(QPen(Qt.GlobalColor.white, 3))
        triangle.setPos(width / 4, height / 2)

        self.bigFont = QFont()
        self.bigFont.setPixelSize(int(height / 16))

        self.smallFont = QFont()
        self.smallFont.setPixelSize(int(height / 22))

        self.digits = []
        for i in range(-2, 3):
            bigText = QGraphicsTextItem("", self)
            bigText.setDefaultTextColor(Qt.GlobalColor.white)
            bigText.setFont(self.bigFont)
            smallText = QGraphicsTextItem("", self)
            smallText.setDefaultTextColor(Qt.GlobalColor.white)
            smallText.setFont(self.smallFont)
            variableText = QGraphicsTextItem("", self)
            variableText.setDefaultTextColor(Qt.GlobalColor.white)
            variableText.setFont(self.smallFont)
            self.digits.append(
                {
                    "index": i,
                    "bigText": bigText,
                    "smallText": smallText,
                    "variableText": variableText,
                }
            )

    def updatePositions(self, altitude):
        if not isinstance(altitude, numbers.Number):
            main = self.digits[2]["bigText"]
            main.setPlainText(str(altitude))
            main.setVisible(True)
            return

        step = self.metersPerGraduation * 2
        baseAlt = (altitude // step) * step
        centerY = self.height * 0.5

        thousands = int(abs(altitude) // 1000)
        hundreds = int((abs(altitude) % 1000) // 100)

        for digit in self.digits:
            altVal = baseAlt + digit["index"] * self.metersPerGraduation
            yOffset = (altitude - altVal) * self.pxPerMeter

            tens = int((abs(altVal) % 100) // 10 * 10)
            text = f"{tens:02d}"

            var = digit["variableText"]
            if var.toPlainText() != text:
                var.setPlainText(text)

            rect = var.boundingRect()
            var.setPos(
                self.width - rect.width() / 2 + 5,
                centerY + yOffset - rect.height() * 0.5,
            )
            var.setVisible(True)

        main = self.digits[2]
        big = main["bigText"]
        small = main["smallText"]

        bigStr = f"-{thousands:02d}" if altitude < 0 else f"{thousands:02d}"
        smallStr = str(hundreds)

        if big.toPlainText() != bigStr:
            big.setPlainText(bigStr)
        if small.toPlainText() != smallStr:
            small.setPlainText(smallStr)

        bigRect = big.boundingRect()
        smallRect = small.boundingRect()

        big.setPos(
            self.width - rect.width() - smallRect.width() - bigRect.width() / 2 + 10,
            centerY - bigRect.height() / 2,
        )
        small.setPos(
            self.width - rect.width() - smallRect.width() / 2 + 25,
            centerY - smallRect.height() / 2,
        )

        big.setVisible(True)
        small.setVisible(True)

    def boundingRect(self):
        return QRectF(
            0, self.height / 2 - self.height / 15, self.width * 2, self.height * 2 / 15
        )

    def shape(self):
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path
