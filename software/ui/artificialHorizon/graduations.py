from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsLineItem, QGraphicsTextItem
from PyQt6.QtGui import QColor, QPen, QFont
from PyQt6.QtCore import Qt, QRectF


class PitchGraduations(QGraphicsItemGroup):
    def __init__(self, parent, width, height):
        super().__init__(parent)

        self.width = width
        self.height = height
        self.pixelsPerDegree = height / 45.0

        self.step = 2.5
        self.span = 20

        self.nbGraduations = int((self.span * 2) / self.step)
        self.graduationsPool = []

        self.lineLengths = {
            10: width / 6,
            5: width / 10,
            "minor": width / 16
        }

        pen = QPen(QColor("#FFFFFF"), 3)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        self.font = QFont("Arial", int(height / 21))

        for _ in range(self.nbGraduations):
            line = QGraphicsLineItem(self)
            line.setPen(pen)

            leftText = QGraphicsTextItem(line)
            leftText.setDefaultTextColor(Qt.GlobalColor.white)
            leftText.setFont(self.font)

            rightText = QGraphicsTextItem(line)
            rightText.setDefaultTextColor(Qt.GlobalColor.white)
            rightText.setFont(self.font)

            self.graduationsPool.append(
                (line, leftText, rightText)
            )

    def updatePositions(self, pitchDeg):
        pitchDeg = ((pitchDeg + 180) % 360) - 180
        
        if pitchDeg > 90:
            displayPitch = 180 - pitchDeg
            isInverted = True
        elif pitchDeg < -90:
            displayPitch = -180 - pitchDeg
            isInverted = True
        else:
            displayPitch = pitchDeg
            isInverted = False

        self.setRotation(180 if isInverted else 0)

        basePitch = round(displayPitch / self.step) * self.step
        startOffset = -(self.nbGraduations // 2)

        for i, (line, leftText, rightText) in enumerate(self.graduationsPool):
            gradPitch = basePitch + (startOffset + i) * self.step

            if gradPitch < -90 or gradPitch > 90:
                line.setVisible(False)
                continue

            relPitch = gradPitch - displayPitch
            
            yPos = -(relPitch * self.pixelsPerDegree)

            line.setPos(0, yPos)

            if abs(yPos) > self.height / 2:
                line.setVisible(False)
                continue

            line.setVisible(True)

            absPitch = abs(gradPitch)
            
            mod10 = absPitch % 10
            mod5 = absPitch % 5

            if mod10 == 0:
                halfLen = self.lineLengths[10]
            elif mod5 == 0:
                halfLen = self.lineLengths[5]
            else:
                halfLen = self.lineLengths["minor"]

            line.setLine(-halfLen, 0, halfLen, 0)

            if mod10 == 0 and absPitch != 0:
                textStr = f"{int(absPitch):02d}"
                leftText.setPlainText(textStr)
                rightText.setPlainText(textStr)

                leftText.setVisible(True)
                rightText.setVisible(True)

                textW = leftText.boundingRect().width()
                textH = leftText.boundingRect().height()

                leftText.setPos(-halfLen - textW - 4, -textH / 2)
                rightText.setPos(halfLen + 4, -textH / 2)
            else:
                leftText.setVisible(False)
                rightText.setVisible(False)