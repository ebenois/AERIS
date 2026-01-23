from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsLineItem, QGraphicsTextItem
from PyQt6.QtGui import QColor, QPen, QFont
from PyQt6.QtCore import Qt


class AltitudeGraduations(QGraphicsItemGroup):     
    def __init__(self, parent=None, width=600):
        super().__init__(parent)

        self.width = width
        self.graduationsData = []

        pen = QPen(QColor("#FFFFFF"), 4)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        font = QFont("Arial", 17)

        for i in range(-10, 10 + 1):
            line = QGraphicsLineItem(-width / 2, 0, -width / 2 + 12, 0, self)
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

    def updatePositions(self, altitude):
        baseAltitude = int(altitude // 100) * 100

        for grad in self.graduationsData:
            offset = grad["index"] * 50
            altitudeValue = baseAltitude + offset

            y_local = altitude - altitudeValue

            grad["line"].setPos(0, y_local)

            if grad["text"]:
                grad["text"].setPlainText(str(int(altitudeValue)))
                grad["text"].setPos(
                    -self.width / 3,
                    y_local - grad["text"].boundingRect().height() / 2
                )
