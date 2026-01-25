from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsLineItem, QGraphicsTextItem
from PyQt6.QtGui import QColor, QPen, QFont
from PyQt6.QtCore import Qt
import math

class DirectionGraduations(QGraphicsItemGroup):
    def __init__(self, parent=None, width=15):
        super().__init__(parent)

        self.width = width
        self.radius = 222
        self.step = 5
        self.span = 60

        self.nbGraduations = (self.span * 2) // self.step + 1
        self.graduationsPool = []

        pen = QPen(QColor("#FFFFFF"), 4)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        self.bigFont = QFont("Arial", 18)
        self.smallFont = QFont("Arial", 13)

        for _ in range(self.nbGraduations):
            text = QGraphicsTextItem("", self)
            text.setDefaultTextColor(Qt.GlobalColor.white)
            
            line = QGraphicsLineItem(
                0,
                -self.radius,
                0,
                -self.radius + width/2,
                self
            )
            line.setPen(pen)

            self.graduationsPool.append({
                "line": line,
                "text": text
            })

    def updatePositions(self, direction):
        baseAngle = round(direction / self.step) * self.step

        startOffset = -(self.nbGraduations // 2)

        for i in range(self.nbGraduations):
            gradAngle = baseAngle + (startOffset + i) * self.step
            
            relAngle = gradAngle - direction
            
            item = self.graduationsPool[i]
            line = item["line"]
            text = item["text"]

            if abs(relAngle) > self.span:
                line.setVisible(False)
                text.setVisible(False)
                continue
            
            line.setVisible(True)

            if gradAngle % 10 == 0:
                line.setLine(
                    0,
                    -self.radius,
                    0,
                    -self.radius + self.width
                )
            else:
                line.setLine(
                    0,
                    -self.radius,
                    0,
                    -self.radius + self.width / 2
                )

            line.setRotation(relAngle)

            if gradAngle % 10 == 0:
                valDisplay = int((gradAngle % 360) / 10)
                text.setPlainText(f"{valDisplay:02d}")
                text.setFont(self.bigFont if valDisplay % 3 == 0 else self.smallFont)
                text.setVisible(True)
                
                angleRad = math.radians(relAngle)             
                
                x = (self.radius - 15) * math.sin(angleRad) - text.boundingRect().width()/2*math.cos(angleRad)
                y = -(self.radius - 15) * math.cos(angleRad) - text.boundingRect().width()/2*math.sin(angleRad)
                
                text.setPos(x, y)
                text.setRotation(relAngle)
            else:
                text.setVisible(False)