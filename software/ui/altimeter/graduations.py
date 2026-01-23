from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsLineItem, QGraphicsTextItem
from PyQt6.QtGui import QColor, QPen, QFont
from PyQt6.QtCore import Qt
import math


class AltitudeGraduations(QGraphicsItemGroup):
    def __init__(self, parent=None, width=600):
        super().__init__(parent)

        self.metersPerGraduation = 100
        self.pixelsPerGraduation = 48
        self.pxPerMeter = self.pixelsPerGraduation / self.metersPerGraduation

        self.width = width
        self.graduationsData = []

        pen = QPen(QColor("#FFFFFF"), 4)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        bigFont = QFont("Arial", 18)
        smallFont = QFont("Arial", 13)

        for i in range(-10, 11):
            line = QGraphicsLineItem(-width / 2, 0, -width / 2 + 12, 0, self)
            line.setPen(pen)

            bigText = None
            smallText = None

            if i % 2 == 0:
                bigText = QGraphicsTextItem("", self)
                bigText.setDefaultTextColor(Qt.GlobalColor.white)
                bigText.setFont(bigFont)

                smallText = QGraphicsTextItem("", self)
                smallText.setDefaultTextColor(Qt.GlobalColor.white)
                smallText.setFont(smallFont)

            self.graduationsData.append({
                "index": i,
                "line": line,
                "bigText": bigText,
                "smallText": smallText,
            })

    def updatePositions(self, altitude):
        baseAltitude = int(altitude // self.metersPerGraduation*2) * self.metersPerGraduation

        for grad in self.graduationsData:
            altitudeValue = baseAltitude + grad["index"] * self.metersPerGraduation

            y_local = (altitude - altitudeValue) * self.pxPerMeter

            grad["line"].setPos(0, y_local)

            bigText = grad["bigText"]
            smallText = grad["smallText"]

            if not bigText:
                continue

            if altitudeValue >= 1000:
                thousands = altitudeValue // 1000
                remainder = altitudeValue % 1000

                bigText.setPlainText(str(thousands))
                bigText.setPos(
                    -self.width / 3,
                    y_local - bigText.boundingRect().height() / 2
                )
                bigText.setVisible(True)

                smallText.setPlainText(f"{remainder:03d}")
                smallText.setPos(
                    -self.width / 3 + bigText.boundingRect().width() - 8,
                    y_local - smallText.boundingRect().height() / 2 +2
                )
                smallText.setVisible(True)
            else:
                bigText.setVisible(False)

                smallText.setPlainText(str(altitudeValue))
                smallText.setPos(
                    -self.width / 3,
                    y_local - smallText.boundingRect().height() / 2
                )
                smallText.setVisible(True)
