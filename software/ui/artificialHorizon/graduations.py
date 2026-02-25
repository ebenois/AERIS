from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsLineItem, QGraphicsTextItem
from PyQt6.QtGui import QColor, QPen, QFont
from PyQt6.QtCore import Qt


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

        self.lenMajor = width / 6
        self.lenMedium = width / 10
        self.lenMinor = width / 16

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

            self.graduationsPool.append((line, leftText, rightText))

    def updatePositions(self, pitchDeg):
        pitchDeg = ((pitchDeg + 180) % 360) - 180

        if pitchDeg > 90:
            displayPitch = 180 - pitchDeg
            self.setRotation(180)
        elif pitchDeg < -90:
            displayPitch = -180 - pitchDeg
            self.setRotation(180)
        else:
            displayPitch = pitchDeg
            self.setRotation(0)

        basePitch = round(displayPitch / self.step)
        centerIndex = self.nbGraduations // 2

        pixelsPerDegree = self.pixelsPerDegree
        halfHeight = self.height / 2
        step = self.step

        for i, (line, leftText, rightText) in enumerate(self.graduationsPool):
            stepIndex = basePitch + (i - centerIndex)
            gradPitch = stepIndex * step

            if not -90 <= gradPitch <= 90:
                line.setVisible(False)
                continue

            relPitch = gradPitch - displayPitch
            yPos = -(relPitch * pixelsPerDegree)

            if abs(yPos) > halfHeight:
                line.setVisible(False)
                continue

            line.setVisible(True)
            line.setPos(0, yPos)

            absStepIndex = abs(stepIndex)

            if absStepIndex % 4 == 0:  # 10°
                halfLen = self.lenMajor
                isMajor = True
            elif absStepIndex % 2 == 0:  # 5°
                halfLen = self.lenMedium
                isMajor = False
            else:
                halfLen = self.lenMinor
                isMajor = False

            line.setLine(-halfLen, 0, halfLen, 0)

            if isMajor and stepIndex != 0:
                textStr = f"{int(abs(gradPitch)):02d}"
                leftText.setPlainText(textStr)
                rightText.setPlainText(textStr)

                leftText.setVisible(True)
                rightText.setVisible(True)

                rect = leftText.boundingRect()
                textW = rect.width()
                textH = rect.height()

                yText = -textH / 2
                leftText.setPos(-halfLen - textW - 4, yText)
                rightText.setPos(halfLen + 4, yText)
            else:
                leftText.setVisible(False)
                rightText.setVisible(False)
