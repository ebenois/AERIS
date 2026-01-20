from PyQt6.QtWidgets import (
    QGraphicsItemGroup,
    QGraphicsEllipseItem,
    QGraphicsLineItem
)
from PyQt6.QtGui import QPen, QColor, QBrush
from PyQt6.QtCore import Qt

from ui.artificialHorizon.background import ArtificialHorizonBackground

ecartMin, ecartMax, outline, dotRadius, lineWidth, lineHeigth = 45, 120, 2, 5, 10, 12

class ArtificialHorizonInstrument(QGraphicsItemGroup):
    def __init__(self):
        super().__init__()

        self.artificialHorizon = ArtificialHorizonBackground()
        self.addToGroup(self.artificialHorizon)

        self.maquette = QGraphicsItemGroup()
        self.addToGroup(self.maquette)

        self.drawIndicatorGeneric(
            color="white",
            penWidth=lineWidth + (outline + 3),
            dotRadiusExtra=outline
        )
        self.drawIndicatorGeneric(
            color="black",
            penWidth=lineWidth
        )

        center = self.boundingRect().center()
        self.setTransformOriginPoint(center)
        self.setPos(-center)

    def drawIndicatorGeneric(self, color, penWidth, dotRadiusExtra=0):
        pen = QPen(QColor(color), penWidth)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        for sign in [-1,1]:
            # Ailes
            wing = QGraphicsLineItem(sign*ecartMax, 0, sign*ecartMin, 0)
            wing.setPen(pen)
            self.maquette.addToGroup(wing)

            # Montants
            montant = QGraphicsLineItem(sign*ecartMin, 0, sign*ecartMin, lineHeigth)
            montant.setPen(pen)
            self.maquette.addToGroup(montant)

        # Point central
        dotR = dotRadius + dotRadiusExtra
        dot = QGraphicsEllipseItem(
            -dotR, -dotR, dotR * 2, dotR * 2
        )
        dot.setBrush(QBrush(QColor(color)))
        dot.setPen(QPen(Qt.PenStyle.NoPen))
        self.maquette.addToGroup(dot)