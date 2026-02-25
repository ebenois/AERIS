from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsLineItem, QGraphicsTextItem
from PyQt6.QtGui import QColor, QPen, QFont
from PyQt6.QtCore import Qt
import math


class DirectionGraduations(QGraphicsItemGroup):
    def __init__(self, size):
        super().__init__()

        self.radius = size / 2
        self.ratioMajor = 14 / 15
        self.ratioMinor = 29 / 30

        self.step = 5
        self.span = 60

        self.nbGraduations = (self.span * 2) // self.step + 1
        self.graduationsPool = []

        pen = QPen(QColor("#FFFFFF"), 4)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        self.bigFont = QFont("Arial", int(size / 20))
        self.smallFont = QFont("Arial", int(size / 30))

        r = self.radius
        rMinor = r * self.ratioMinor

        for _ in range(self.nbGraduations):
            text = QGraphicsTextItem("", self)
            text.setDefaultTextColor(Qt.GlobalColor.white)

            line = QGraphicsLineItem(0, -r, 0, -rMinor, self)
            line.setPen(pen)

            self.graduationsPool.append((line, text))

    def updatePositions(self, direction):
        step = self.step
        span = self.span
        radius = self.radius
        ratioMajor = self.ratioMajor
        ratioMinor = self.ratioMinor

        rMajor = radius * ratioMajor
        rMinor = radius * ratioMinor

        baseAngle = round(direction / step) * step
        centerIndex = self.nbGraduations // 2

        for i, (line, text) in enumerate(self.graduationsPool):
            gradAngle = baseAngle + (i - centerIndex) * step
            relAngle = gradAngle - direction

            if abs(relAngle) > span:
                line.setVisible(False)
                text.setVisible(False)
                continue

            line.setVisible(True)

            isMajor = gradAngle % 10 == 0

            if isMajor:
                line.setLine(0, -rMajor, 0, -radius)
            else:
                line.setLine(0, -rMinor, 0, -radius)

            line.setRotation(relAngle)

            if isMajor:
                value = (gradAngle % 360) // 10
                text.setPlainText(f"{int(value):02d}")
                text.setFont(self.bigFont if value % 3 == 0 else self.smallFont)
                text.setVisible(True)

                angleRad = math.radians(relAngle)
                sinA = math.sin(angleRad)
                cosA = math.cos(angleRad)

                rect = text.boundingRect()
                halfW = rect.width() / 2
                halfH = rect.height() / 2

                x = rMajor * sinA - halfW * cosA
                y = -rMajor * cosA - halfH * sinA

                text.setPos(x, y)
                text.setRotation(relAngle)
            else:
                text.setVisible(False)
