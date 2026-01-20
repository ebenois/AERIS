from PyQt6.QtWidgets import (
    QGraphicsItemGroup,
    QGraphicsEllipseItem,
    QGraphicsLineItem
)
from PyQt6.QtGui import QPen, QColor, QBrush
from PyQt6.QtCore import Qt

ecartMin, ecartMax, outline, dotRadius, lineWidth, lineHeigth = 0.15, 0.4, 3, 13, 21, 25

class ArtificialHorizonInstrument(QGraphicsItemGroup):
    def __init__(self, size=600, scale=1.0):
        super().__init__()

        self.maquette = QGraphicsItemGroup()
        self.addToGroup(self.maquette)

        self.drawIndicatorGeneric(
            size=size,
            color="white",
            pen_width=lineWidth + (outline + 3),
            dot_radius_extra=outline
        )
        self.drawIndicatorGeneric(
            size=size,
            color="black",
            pen_width=lineWidth
        )

        self.setScale(scale)
        center = self.boundingRect().center()
        self.setTransformOriginPoint(center)
        self.setPos(-center)


    def drawIndicatorGeneric(self, size, color, pen_width, dot_radius_extra=0):
        pen = QPen(QColor(color), pen_width)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        # Ailes
        line_l = QGraphicsLineItem(-size * ecartMax, 0, -size * ecartMin, 0)
        line_l.setPen(pen)
        self.maquette.addToGroup(line_l)

        line_r = QGraphicsLineItem(size * ecartMin, 0, size * ecartMax, 0)
        line_r.setPen(pen)
        self.maquette.addToGroup(line_r)

        # Montants
        v_l = QGraphicsLineItem(-size * ecartMin, 0, -size * ecartMin, lineHeigth)
        v_l.setPen(pen)
        self.maquette.addToGroup(v_l)

        v_r = QGraphicsLineItem(size * ecartMin, 0, size * ecartMin, lineHeigth)
        v_r.setPen(pen)
        self.maquette.addToGroup(v_r)

        # Point central
        dot_r = dotRadius + dot_radius_extra
        dot = QGraphicsEllipseItem(
            -dot_r, -dot_r, dot_r * 2, dot_r * 2
        )
        dot.setBrush(QBrush(QColor(color)))
        dot.setPen(QPen(Qt.PenStyle.NoPen))
        self.maquette.addToGroup(dot)