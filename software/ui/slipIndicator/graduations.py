from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsLineItem
from PyQt6.QtGui import QColor, QPen
from PyQt6.QtCore import Qt
import math


class SlipGraduations(QGraphicsItemGroup):
    def __init__(self, width, height):
        super().__init__()

        self.width = width / 15
        self.radius = height
        self.step = 10
        self.span = 60

        self.nbGraduations = (self.span * 2) // self.step + 1
        self.graduationsPool = []

        pen = QPen(QColor("#FFFFFF"), 4)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        for _ in range(self.nbGraduations):
            line = QGraphicsLineItem(self)
            line.setPen(pen)

            self.graduationsPool.append(line)

        offset = -(self.nbGraduations // 2)

        for i, line in enumerate(self.graduationsPool):
            grad = (offset + i) * self.step

            if abs(grad) == 0:
                line.setVisible(False)
                continue

            if grad % 30 == 0:
                line.setLine(0, -self.radius, 0, -self.radius + self.width * 3 / 4)
            else:
                line.setLine(
                    0,
                    -self.radius + self.width / 4,
                    0,
                    -self.radius + self.width * 3 / 4,
                )

            line.setRotation(grad * math.tanh(width / (2 * self.radius)))
            self.setPos(width / 2, height)
