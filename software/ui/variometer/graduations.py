from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsLineItem, QGraphicsTextItem
from PyQt6.QtGui import QColor, QPen, QFont
from PyQt6.QtCore import Qt
import math

class RiseGraduations(QGraphicsItemGroup):
    def __init__(self, parent=None, width=600):
        super().__init__(parent)

        self.width = width
        self.step = 0.5
        self.span = 6

        self.nbGraduations = int(self.span * 2 / self.step) + 1
        self.graduations = []

        pen = QPen(QColor("#FFFFFF"), 2, cap=Qt.PenCapStyle.RoundCap)
        font = QFont("Arial", 12)

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

            pxPerUnit = 145

            if rel < 0:
                y = math.log10(abs(rel) + 1) * pxPerUnit
            elif rel > 0:
                y = -math.log10(abs(rel) + 1) * pxPerUnit
            else:
                y = 0

            isInt = grad.is_integer()

            line.setLine(-10, 0, 2 if isInt else -6, 0)
            line.setPos(0, y)
            line.show()

            if isInt:
                text.setPlainText(str(int(abs(grad))))
                text.setPos(-26, y - text.boundingRect().height() / 2)
                text.show()
            else:
                text.hide()
