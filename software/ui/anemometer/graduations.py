from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsLineItem, QGraphicsTextItem
from PyQt6.QtGui import QColor, QPen, QFont
from PyQt6.QtCore import Qt
import math


class SpeedGraduations(QGraphicsItemGroup):
    def __init__(self, parent=None, width=600):
        super().__init__(parent)

        self.knotsPerGraduation = 10
        self.pixelsPerGraduation = 34
        self.pxPerKnot = self.pixelsPerGraduation / self.knotsPerGraduation

        self.width = width
        self.graduationsData = []

        pen = QPen(QColor("#FFFFFF"), 4)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        font = QFont("Arial", 15)

        for i in range(-5, 8):
            line = QGraphicsLineItem(width / 2, 0, width / 2 - 12, 0, self)
            line.setPen(pen)

            text = None

            if i % 2 == 0:
                text = QGraphicsTextItem("", self)
                text.setDefaultTextColor(Qt.GlobalColor.white)
                text.setFont(font)

            self.graduationsData.append({
                "index": i,
                "line": line,
                "text": text
            })

    def updatePositions(self, speed):
        step = self.knotsPerGraduation * 2

        baseSpeed = (speed // step) * step

        for grad in self.graduationsData:
            speedValue = baseSpeed + grad["index"] * self.knotsPerGraduation

            y_local = (speed - speedValue) * self.pxPerKnot

            grad["line"].setPos(0, y_local)

            text = grad["text"]

            if text is not None:
                text.setPlainText(str(speedValue))
                text.setPos(
                    self.width / 3 - 45,
                    y_local - text.boundingRect().height() / 2
                )
                text.setVisible(True)
