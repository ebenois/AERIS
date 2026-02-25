from PyQt6.QtWidgets import (
    QGraphicsItemGroup,
    QGraphicsItem,
    QGraphicsLineItem,
    QGraphicsTextItem,
)
from PyQt6.QtGui import QColor, QPen, QFont, QPainterPath
from PyQt6.QtCore import Qt, QRectF


class SpeedGraduations(QGraphicsItemGroup):
    def __init__(self, width, height):
        super().__init__()

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemClipsChildrenToShape, True)

        self.width = width
        self.height = height
        self.step = 10
        self.span = 70

        self.nbGraduations = (self.span * 2) // self.step + 1
        self.graduationsPool = []

        pen = QPen(QColor("#FFFFFF"), 4)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        self.font = QFont("Arial", int(height / 21))

        for _ in range(self.nbGraduations):
            line = QGraphicsLineItem(width * 7 / 8, 0, width, 0, self)
            line.setPen(pen)

            text = QGraphicsTextItem("", self)
            text.setDefaultTextColor(Qt.GlobalColor.white)
            text.setFont(self.font)

            self.graduationsPool.append({"line": line, "text": text})

    def updatePositions(self, speed):
        halfHeight = self.height * 0.5
        scale = halfHeight / self.span
        baseSpeed = round(speed / self.step) * self.step
        startOffset = -(self.nbGraduations // 2)

        for i, item in enumerate(self.graduationsPool):
            gradSpeed = baseSpeed + (startOffset + i) * self.step
            relSpeed = gradSpeed - speed

            if abs(relSpeed) > self.span:
                item["line"].setVisible(False)
                item["text"].setVisible(False)
                continue

            y = halfHeight - relSpeed * scale
            item["line"].setVisible(True)
            item["line"].setPos(0, y)

            text = item["text"]
            if gradSpeed % 20 == 0:
                text.setPlainText(str(gradSpeed))
                rect = text.boundingRect()
                text.setPos(self.width / 3 - 45, y - rect.height() / 2)
                text.setVisible(True)
            else:
                text.setVisible(False)

    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)

    def shape(self):
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path
