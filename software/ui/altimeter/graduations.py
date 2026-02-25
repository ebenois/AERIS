from PyQt6.QtWidgets import (
    QGraphicsItemGroup,
    QGraphicsLineItem,
    QGraphicsTextItem,
    QGraphicsItem,
)
from PyQt6.QtGui import QColor, QPen, QFont, QPainterPath
from PyQt6.QtCore import Qt, QRectF


class AltitudeGraduations(QGraphicsItemGroup):
    def __init__(self, width, height):
        super().__init__()

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemClipsChildrenToShape, True)

        self.height = height
        self.width = width
        self.step = 100
        self.span = 500

        self.nbGraduations = (self.span * 2) // self.step + 1
        self.graduationsPool = []

        pen = QPen(QColor("#FFFFFF"), 4)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        self.bigFont = QFont("Arial", int(height / 22))
        self.smallFont = QFont("Arial", int(height / 28))

        for _ in range(self.nbGraduations):
            line = QGraphicsLineItem(0, 0, width / 8, 0, self)
            line.setPen(pen)

            bigText = QGraphicsTextItem("", self)
            bigText.setDefaultTextColor(Qt.GlobalColor.white)
            bigText.setFont(self.bigFont)

            smallText = QGraphicsTextItem("", self)
            smallText.setDefaultTextColor(Qt.GlobalColor.white)
            smallText.setFont(self.smallFont)

            self.graduationsPool.append(
                {"line": line, "bigText": bigText, "smallText": smallText}
            )

    def updatePositions(self, altitude):
        halfHeight = self.height * 0.5
        scale = halfHeight / self.span
        baseAlt = round(altitude / self.step) * self.step
        start = -(self.nbGraduations // 2)

        for i, item in enumerate(self.graduationsPool):
            gradAlt = baseAlt + (start + i) * self.step
            relAlt = gradAlt - altitude

            if abs(relAlt) > self.span:
                item["line"].setVisible(False)
                item["bigText"].setVisible(False)
                item["smallText"].setVisible(False)
                continue

            y = halfHeight - relAlt * scale
            item["line"].setVisible(True)
            item["line"].setPos(0, y)

            if gradAlt % 200 == 0:
                absAlt = abs(gradAlt)
                thousands = absAlt // 1000
                remainder = absAlt % 1000

                prefix = "-" if gradAlt < 0 else ""
                bigStr = f"{prefix}{thousands:02d}"
                smallStr = f"{remainder:03d}"

                big = item["bigText"]
                small = item["smallText"]

                if big.toPlainText() != bigStr:
                    big.setPlainText(bigStr)
                if small.toPlainText() != smallStr:
                    small.setPlainText(smallStr)

                smallRect = small.boundingRect()
                bigRect = big.boundingRect()

                small.setPos(
                    self.width - smallRect.width(), y - smallRect.height() * 0.5
                )

                big.setPos(
                    self.width - smallRect.width() - bigRect.width() * 0.875,
                    y - bigRect.height() * 0.5,
                )

                big.setVisible(True)
                small.setVisible(True)
            else:
                item["bigText"].setVisible(False)
                item["smallText"].setVisible(False)

    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)

    def shape(self):
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path
