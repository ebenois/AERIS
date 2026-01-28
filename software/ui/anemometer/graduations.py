from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsLineItem, QGraphicsTextItem
from PyQt6.QtGui import QColor, QPen, QFont
from PyQt6.QtCore import Qt
import math


class SpeedGraduations(QGraphicsItemGroup):
    def __init__(self, parent=None, width=600):
        super().__init__(parent)

        self.width = width
        self.step = 10
        self.span = 70

        self.nbGraduations = (self.span * 2) // self.step + 1
        self.graduationsPool = []

        pen = QPen(QColor("#FFFFFF"), 4)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        self.font = QFont("Arial", 15)

        for _ in range(self.nbGraduations):
            line = QGraphicsLineItem(width / 2, 0, width / 2 - 12, 0, self)
            line.setPen(pen)

            text = QGraphicsTextItem("", self)
            text.setDefaultTextColor(Qt.GlobalColor.white)
            text.setFont(self.font)

            self.graduationsPool.append({
                "line": line,
                "text": text
            })

    def updatePositions(self, speed):
        baseSpeed = round(speed / self.step) * self.step
        startOffset = -(self.nbGraduations // 2)

        for i in range(self.nbGraduations):
            gradSpeed = baseSpeed + (startOffset + i) * self.step
            relSpeed = gradSpeed - speed
            
            item = self.graduationsPool[i]
            line = item["line"]
            text = item["text"]

            if abs(relSpeed) > self.span:
                line.setVisible(False)
                text.setVisible(False)
                continue
            
            line.setVisible(True)

            y = relSpeed * -3.4

            line.setPos(0, y)

            if gradSpeed % 20 == 0:
                text.setPlainText(str(gradSpeed))
                text.setPos(
                    self.width / 3 - 45,
                    y - text.boundingRect().height() / 2
                )
                text.setVisible(True)
            else:
                text.setVisible(False)
