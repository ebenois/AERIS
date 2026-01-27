from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsLineItem, QGraphicsTextItem
from PyQt6.QtGui import QColor, QPen, QFont
from PyQt6.QtCore import Qt
import math

class PitchGraduations(QGraphicsItemGroup):
    def __init__(self, parent=None, width=24):
        super().__init__(parent)

        self.width = width
        self.step = 2.5
        self.span = 30

        self.nbGraduations = (self.span * 2) // int(self.step) + 1
        self.graduationsPool = []

        pen = QPen(QColor("#FFFFFF"), 3)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        self.font = QFont("Arial", 18)

        for _ in range(self.nbGraduations):
            line = QGraphicsLineItem(-width/2, 0, width/2, 0, self)
            line.setPen(pen)

            leftText = QGraphicsTextItem("", line)
            leftText.setDefaultTextColor(Qt.GlobalColor.white)
            rigthText = QGraphicsTextItem("", line)
            rigthText.setDefaultTextColor(Qt.GlobalColor.white)

            self.graduationsPool.append({
                "line": line,
                "leftText": leftText,
                "rigthText": rigthText
            })

    def updatePositions(self, pitchDeg):
        basePitch = round(pitchDeg / self.step) * self.step
        startOffset = -(self.nbGraduations // 2)

        for i in range(self.nbGraduations):
            gradPitch = basePitch + (startOffset + i) * self.step
            relPitch = gradPitch - pitchDeg

            item = self.graduationsPool[i]
            line = item["line"]
            leftText = item["leftText"]
            rigthText = item["rigthText"]

            if abs(relPitch) > self.span:
                line.setVisible(False)
                leftText.setVisible(False)
                rigthText.setVisible(False)
                continue

            line.setVisible(True)

            if gradPitch % 10 == 0:
                line.setLine(-self.width*4/2, 0, self.width*4/2, 0)
            elif gradPitch % 5 == 0:
                line.setLine(-self.width*2/2, 0, self.width*2/2, 0)
            else:
                line.setLine(-self.width/2, 0, self.width/2, 0)

            y = relPitch * 6.5

            line.setPos(0, -y)
            
            if abs(pitchDeg)>90:
                gradPitch=180-gradPitch
                if abs(pitchDeg)<270:
                    line.setRotation(180)
                else:
                    gradPitch=180+gradPitch
                    line.setRotation(0)
            else:
                line.setRotation(0)

            if gradPitch % 10 == 0 and gradPitch != 0:
                leftText.setPlainText(f"{int(abs(gradPitch)):02d}")
                leftText.setFont(self.font)
                leftText.setVisible(True)

                rigthText.setPlainText(f"{int(abs(gradPitch)):02d}")
                rigthText.setFont(self.font)
                rigthText.setVisible(True)

                hDistX = 40
                hDistY = 18

                leftTextX = hDistX*2 + leftText.boundingRect().width()/2
                leftTextY = hDistY

                leftText.setPos(-leftTextX, -leftTextY)

                rigthTextX = -hDistX - rigthText.boundingRect().width()/2
                rigthTextY = hDistY

                rigthText.setPos(-rigthTextX, -rigthTextY)
            else:
                leftText.setVisible(False)
                rigthText.setVisible(False)

            if abs(gradPitch)>90:
                line.setVisible(False)
