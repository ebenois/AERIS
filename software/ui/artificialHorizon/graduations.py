from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsLineItem, QGraphicsTextItem
from PyQt6.QtGui import QColor, QPen, QFont
from PyQt6.QtCore import Qt
import math

class PitchGraduations(QGraphicsItemGroup):
    def __init__(self,parent, width, height):
        super().__init__(parent)

        self.width = width
        self.height = height
        self.step = 2.5
        self.span = 20

        self.nbGraduations = int((self.span * 2) / self.step)
        print(self.nbGraduations)
        self.graduationsPool = []

        pen = QPen(QColor("#FFFFFF"), 3)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        self.font = QFont("Arial", int(height/21))

        for _ in range(self.nbGraduations):
            line = QGraphicsLineItem(self)
            line.setPen(pen)

            leftText = QGraphicsTextItem("", line)
            leftText.setDefaultTextColor(Qt.GlobalColor.white)
            leftText.setFont(self.font)
            rigthText = QGraphicsTextItem("", line)
            rigthText.setDefaultTextColor(Qt.GlobalColor.white)
            rigthText.setFont(self.font)

            self.graduationsPool.append({
                "line": line,
                "leftText": leftText,
                "rigthText": rigthText
            })

    def updatePositions(self, pitchDeg):
        pitchDeg = ((pitchDeg + 180) % 360) - 180
        
        isInverted = abs(pitchDeg) > 90

        basePitch = round(pitchDeg / self.step) * self.step
        startOffset = -(self.nbGraduations // 2)

        for i in range(self.nbGraduations):
            gradPitch = basePitch + (startOffset + i) * self.step
            
            relPitch = gradPitch - pitchDeg
            
            item = self.graduationsPool[i]
            line = item["line"]
            leftText = item["leftText"]
            rigthText = item["rigthText"]

            displayPitch = gradPitch
            if displayPitch > 90: displayPitch = 180 - displayPitch
            if displayPitch < -90: displayPitch = -180 - displayPitch

            if isInverted:
                line.setRotation(180)
            else:
                line.setRotation(0)

            if displayPitch % 10 == 0:
                line.setLine(-self.width/6, 0, self.width/6, 0)
            elif displayPitch % 5 == 0:
                line.setLine(-self.width/10, 0, self.width/10, 0)
            else:
                line.setLine(-self.width/16, 0, self.width/16, 0)

            y = relPitch * self.height/(2*22.5)
            line.setPos(0, -y)

            val = int(abs(displayPitch))
            if displayPitch % 10 == 0 and val != 0:
                textStr = f"{val:02d}"
                leftText.setPlainText(textStr)
                rigthText.setPlainText(textStr)
                leftText.setVisible(True)
                rigthText.setVisible(True)

                if isInverted:
                    leftText.setPos(self.width/6, -leftText.boundingRect().width()/2) 
                    rigthText.setPos(-self.width/6 - rigthText.boundingRect().width(), -rigthText.boundingRect().height()/2)
                else:
                    leftText.setPos(-self.width/6 - leftText.boundingRect().width(), -leftText.boundingRect().width()/2)
                    rigthText.setPos(self.width/6, -rigthText.boundingRect().height()/2)
            else:
                leftText.setVisible(False)
                rigthText.setVisible(False)