from PyQt6.QtWidgets import (
    QGraphicsItemGroup,
    QGraphicsItem,
    QGraphicsLineItem,
    QGraphicsTextItem,
)
from PyQt6.QtGui import QColor, QPen, QFont, QPainterPath
from PyQt6.QtCore import Qt, QRectF
import math


class RiseGraduations(QGraphicsItemGroup):
    def __init__(self, width, height):
        super().__init__()

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemClipsChildrenToShape, True)

        self.width = width
        self.height = height
        self.step = 0.5
        self.span = 6

        self.nbGraduations = int(self.span * 2 / self.step) + 1
        self.graduations = []

        pen = QPen(QColor("#FFFFFF"), int(height / 150))
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        self.font = QFont()
        self.font.setPixelSize(int(height / 20))

        for _ in range(self.nbGraduations):
            line = QGraphicsLineItem(self)
            line.setPen(pen)

            text = QGraphicsTextItem(self)
            text.setDefaultTextColor(Qt.GlobalColor.white)
            text.setFont(self.font)

            self.graduations.append((line, text))

        offset = -(self.nbGraduations // 2)

        for i, (line, text) in enumerate(self.graduations):
            grad = (offset + i) * self.step

            if abs(grad) > self.span:
                line.hide()
                text.hide()
                continue

            pxPerUnit = height / (2 * math.log10(7)) * (14 / 15)

            if grad < 0:
                y = math.log10(abs(grad) + 1) * pxPerUnit
            elif grad > 0:
                y = -math.log10(abs(grad) + 1) * pxPerUnit
            else:
                y = 0

            isInt = grad.is_integer()

            line.setLine(width / 4, 0, width / 2 if isInt else width / 3, 0)
            line.setPos(0, y + height / 2)
            line.show()

            if isInt and (int(abs(grad)) % 2 == 0 or int(abs(grad)) == 1):
                text.setPlainText(str(int(abs(grad))))
                text.setPos(0, y + height / 2 - text.boundingRect().height() / 2)
                text.show()
            else:
                text.hide()

    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)

    def shape(self):
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path
