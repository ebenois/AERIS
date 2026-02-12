from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsLineItem, QGraphicsTextItem
from PyQt6.QtGui import QColor, QPen, QFont
from PyQt6.QtCore import Qt
import math

class RiseGraduations(QGraphicsItemGroup):
    def __init__(self, width, height):
        super().__init__() #parent

        self.width = width
        self.step = 0.5
        self.span = 6

        self.nbGraduations = int(self.span * 2 / self.step) + 1
        self.graduations = []

        pen = QPen(QColor("#FFFFFF"), int(height/150), cap=Qt.PenCapStyle.RoundCap)
        font = QFont("Arial", int(height/20))

        for _ in range(self.nbGraduations):
            line = QGraphicsLineItem(self)
            line.setPen(pen)

            text = QGraphicsTextItem(self)
            text.setDefaultTextColor(Qt.GlobalColor.white)
            text.setFont(font)

            self.graduations.append((line, text))

        base = 0
        offset = -(self.nbGraduations // 2)

        for i, (line, text) in enumerate(self.graduations):
            grad = base + (offset + i) * self.step
            rel = grad - base

            if abs(rel) > self.span:
                line.hide()
                text.hide()
                continue

            pxPerUnit = height/(2 * math.log10(7)) * (14/15)

            if rel < 0:
                y = math.log10(abs(rel) + 1) * pxPerUnit
            elif rel > 0:
                y = -math.log10(abs(rel) + 1) * pxPerUnit
            else:
                y = 0

            isInt = grad.is_integer()

            line.setLine(width/4, 0, width/2 if isInt else width/3, 0)
            line.setPos(0, y + height/2)
            line.show()

            if isInt and (int(abs(grad))%2==0 or int(abs(grad))==1):
                text.setPlainText(str(int(abs(grad))))
                text.setPos(0, y + height/2 - text.boundingRect().height() / 2)
                text.show()
            else:
                text.hide()
