from PyQt6.QtWidgets import QGraphicsItem, QGraphicsItemGroup, QGraphicsRectItem, QGraphicsLineItem
from PyQt6.QtGui import QPen, QBrush, QColor, QPainterPath
from PyQt6.QtCore import Qt, QRectF

class ArtificialHorizonBackground(QGraphicsItem):
    def __init__(self):
        super().__init__()
        self.size = 310

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemClipsChildrenToShape, True)

        self.pitchItems = QGraphicsItemGroup(self)
        self.rollItems = QGraphicsItemGroup(self.pitchItems)

        width, height = self.size*2, self.size*2

        self.sky = QGraphicsRectItem(-width / 2, -height, width, height, self.rollItems)
        self.sky.setBrush(QBrush(QColor("#0080FF")))
        self.sky.setPen(QPen(Qt.PenStyle.NoPen))

        self.ground = QGraphicsRectItem(-width / 2, 0, width, height, self.rollItems)
        self.ground.setBrush(QBrush(QColor("#804000")))
        self.ground.setPen(QPen(Qt.PenStyle.NoPen))

        penHorizon = QPen(QColor("white"), 3)
        self.horizon = QGraphicsLineItem(-width / 2, 0, width / 2, 0, self.rollItems)
        self.horizon.setPen(penHorizon)

    def boundingRect(self):
        return QRectF(-self.size / 2, -self.size / 2, self.size, self.size)

    def shape(self):
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path

    def paint(self, painter, option, widget):
        pass