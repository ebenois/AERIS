from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsLineItem, QGraphicsTextItem
from PyQt6.QtGui import QColor, QPen, QFont
from PyQt6.QtCore import Qt
import math


class AltitudeGraduations(QGraphicsItemGroup):
    def __init__(self, width, height):
        super().__init__()

        self.height = height
        self.width = width
        self.step = 100
        self.span = 500

        self.nbGraduations = (self.span * 2) // self.step + 1
        self.graduationsPool = []

        pen = QPen(QColor("#FFFFFF"), 4)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        self.bigFont = QFont("Arial", int(height/22))
        self.smallFont = QFont("Arial", int(height/28))

        for _ in range(self.nbGraduations):
            line = QGraphicsLineItem(0, 0, width / 8, 0, self)
            line.setPen(pen)

            bigText = QGraphicsTextItem("", self)
            bigText.setDefaultTextColor(Qt.GlobalColor.white)
            bigText.setFont(self.bigFont)

            smallText = QGraphicsTextItem("", self)
            smallText.setDefaultTextColor(Qt.GlobalColor.white)
            smallText.setFont(self.smallFont)

            self.graduationsPool.append({
                "line": line,
                "bigText": bigText,
                "smallText": smallText
            })

    def updatePositions(self, altitude):
        baseAltitude = round(altitude / self.step) * self.step
        startOffset = -(self.nbGraduations // 2)

        for i in range(self.nbGraduations):
            gradAltitude = baseAltitude + (startOffset + i) * self.step
            relAltitude = gradAltitude - altitude
            
            item = self.graduationsPool[i]
            line = item["line"]
            bigText = item["bigText"]
            smallText = item["smallText"]

            if abs(relAltitude) > self.span:
                line.setVisible(False)
                bigText.setVisible(False)
                smallText.setVisible(False)
                continue
            
            line.setVisible(True)

            y = self.height/2 - relAltitude * (self.height/2)/self.span

            line.setPos(0, y)

            if gradAltitude % 200 == 0:
                abs_alt = abs(gradAltitude)
                thousands = abs_alt // 1000
                remainder = abs_alt % 1000

                if gradAltitude < 0:
                    str_thousands = f"-{thousands:02d}" 
                else:
                    str_thousands = f"{thousands:02d}"

                smallText.setPlainText(f"{remainder:03d}")
                smallText.setPos(
                    self.width - smallText.boundingRect().width(),
                    y - smallText.boundingRect().height() / 2 + 2
                )
                smallText.setVisible(True)

                bigText.setPlainText(str_thousands)
                bigText.setPos(
                    self.width - smallText.boundingRect().width() - bigText.boundingRect().width() * 7/8,
                    y - bigText.boundingRect().height() / 2
                )
                bigText.setVisible(True)
            else:
                smallText.setVisible(False)
                bigText.setVisible(False)