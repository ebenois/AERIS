from PyQt6.QtWidgets import (
    QGraphicsItemGroup,
    QGraphicsEllipseItem,
    QGraphicsLineItem
)
from PyQt6.QtGui import QPen, QColor, QBrush
from PyQt6.QtCore import Qt

class ArtificialHorizonInstrument(QGraphicsItemGroup):
    def __init__(self, size=600):
        super().__init__()
