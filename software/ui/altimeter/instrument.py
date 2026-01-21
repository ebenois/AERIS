from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsRectItem, QGraphicsItem, QGraphicsLineItem
from PyQt6.QtGui import QBrush, QColor, QPen, QPainterPath
from PyQt6.QtCore import Qt, QRectF

RECT_W, RECT_H = 70, 410

class AltimeterInstrument(QGraphicsItemGroup):
    def __init__(self):
        super().__init__()

        self.rect = QGraphicsRectItem(
            -RECT_W / 2, -RECT_H / 2,
            RECT_W, RECT_H
        )
        
        self.rect.setBrush(QBrush(QColor("#808080")))
        self.rect.setPen(QPen(Qt.PenStyle.NoPen))
        self.addToGroup(self.rect)

        self.setTransformOriginPoint(0, 0)
