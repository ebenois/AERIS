from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsLineItem, QGraphicsTextItem
from PyQt6.QtGui import QColor, QPen, QFont
from PyQt6.QtCore import Qt

class AltitudeGraduations(QGraphicsItemGroup):
    def __init__(self, parent=None, width=600):
        super().__init__(parent)
        self.graduationsData = []
        
        pen = QPen(QColor("#FFFFFF"), 4)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        font = QFont("Arial", 17)

        for i in range(-100*2, 100*2):
            altitudeValue = i * 50
            
            line = QGraphicsLineItem(-width/2, 0, -width/2+10, 0, self)
            line.setPen(pen)

            text = None
            if i % 2 == 0:
                text = QGraphicsTextItem(str(int(altitudeValue)), self)
                text.setDefaultTextColor(Qt.GlobalColor.white)
                text.setFont(font)

            self.graduationsData.append({
                'line': line,
                'text': text,
                'width': width,
                'altitudeLevel': altitudeValue
            })

    def updatePositions(self, altitude):
        for grad in self.graduationsData:
            altitudeValue = grad['altitudeLevel']

            yLocal = (altitude - altitudeValue)

            grad['line'].setPos(0, yLocal)

            if grad['text']:
                t = grad['text']
                width = grad['width']
                
                t.setPos(-width/3, yLocal - t.boundingRect().height() / 2)

