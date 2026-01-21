from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsRectItem, QGraphicsItem, QGraphicsLineItem
from PyQt6.QtGui import QBrush, QColor, QPen, QPainterPath
from PyQt6.QtCore import Qt, QRectF

from ui.altimeter.graduations import AltitudeGraduations

class AltimeterInstrument(QGraphicsItemGroup):
    def __init__(self):
        super().__init__()
        self.width = 70
        self.height = 410

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemClipsChildrenToShape, True)

        self.rect = QGraphicsRectItem(
            -self.width / 2, -self.height / 2,
            self.width, self.height
        )
        
        self.rect.setBrush(QBrush(QColor("#808080")))
        self.rect.setPen(QPen(Qt.PenStyle.NoPen))
        self.addToGroup(self.rect)

        self.setTransformOriginPoint(0, 0)

        self.graduations = AltitudeGraduations(parent=self, width=self.width)
        self.addToGroup(self.graduations)

        self.mark = QGraphicsItemGroup()
        self.addToGroup(self.mark)
        self.drawMark()

    def drawMark(self, size=600):
        pen = QPen(QColor("#FF00FF"), 3)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        for sign in [-1,1]:
            line_t = QGraphicsLineItem(-size/12, -25*sign, -size/30, -25*sign)
            line_t.setPen(pen)
            self.mark.addToGroup(line_t)

            line_r = QGraphicsLineItem(-size/30, -25*sign, -size/30, 0)
            line_r.setPen(pen)
            self.mark.addToGroup(line_r)

            line_l = QGraphicsLineItem(-size/12, -25*sign, -size/12, -10*sign)
            line_l.setPen(pen)
            self.mark.addToGroup(line_l)

            line_d = QGraphicsLineItem(-size/12, -10*sign, -size/15, 0)
            line_d.setPen(pen)
            self.mark.addToGroup(line_d)

    def updatePositions(self, altitude):
        self.graduations.updatePositions(altitude)

    def boundingRect(self,width=70,height=410):
        return QRectF(-width, -height / 2, width*2, height)

    def shape(self):
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path