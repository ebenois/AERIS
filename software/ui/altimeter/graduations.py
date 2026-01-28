from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsLineItem, QGraphicsTextItem
from PyQt6.QtGui import QColor, QPen, QFont
from PyQt6.QtCore import Qt
import math


class AltitudeGraduations(QGraphicsItemGroup):
    def __init__(self, parent=None, width=600):
        super().__init__(parent)

        self.width = width
        self.step = 100
        self.span = 500

        self.nbGraduations = (self.span * 2) // self.step + 1
        self.graduationsPool = []

        pen = QPen(QColor("#FFFFFF"), 4)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        self.bigFont = QFont("Arial", 18)
        self.smallFont = QFont("Arial", 13)

        for _ in range(self.nbGraduations):
            line = QGraphicsLineItem(-width / 2, 0, -width / 2 + 12, 0, self)
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

            y = relAltitude * -0.48

            line.setPos(0, y)

            if gradAltitude % 200 == 0:
                if gradAltitude >= 1000:
                    thousands = gradAltitude // 1000
                    remainder = gradAltitude % 1000

                    bigText.setPlainText(str(thousands))
                    bigText.setPos(
                        -self.width / 3,
                        y - bigText.boundingRect().height() / 2
                    )
                    bigText.setVisible(True)

                    smallText.setPlainText(f"{remainder:03d}")
                    smallText.setPos(
                        -self.width / 3 + bigText.boundingRect().width() - 8,
                        y - smallText.boundingRect().height() / 2 + 2
                    )
                    smallText.setVisible(True)
                else:
                    bigText.setVisible(False)

                    smallText.setPlainText(str(gradAltitude))
                    smallText.setPos(
                        -self.width / 3,
                        y - smallText.boundingRect().height() / 2
                    )
                    smallText.setVisible(True)
            else:
                bigText.setVisible(False)
                smallText.setVisible(False)

