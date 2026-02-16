from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsLineItem, QGraphicsTextItem, QGraphicsRectItem, QGraphicsItem, QGraphicsPolygonItem
from PyQt6.QtGui import QColor, QPen, QFont, QBrush, QPainterPath, QPolygonF
from PyQt6.QtCore import Qt, QRectF, QPointF
import numbers


class AltitudeIndicator(QGraphicsItemGroup):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height

        self.metersPerGraduation = 20
        self.pixelsPerGraduation = 40
        self.pxPerMeter = self.pixelsPerGraduation / self.metersPerGraduation

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemClipsChildrenToShape, True)

        triangle = QGraphicsPolygonItem()
        self.addToGroup(triangle)

        polygon = QPolygonF([
            QPointF(0, -height/15),
            QPointF(-width/7, 0),
            QPointF(0, height/15),
            QPointF(width, height/15),
            QPointF(width, -height/15),
        ])

        triangle.setPolygon(polygon)
        triangle.setBrush(QBrush(Qt.GlobalColor.black))
        triangle.setPen(QPen(Qt.GlobalColor.white, 3))
        triangle.setPos(width/4,height/2)

        self.bigFont = QFont("Arial", int(height/20))
        self.smallFont = QFont("Arial", int(height/28))

        self.digits = []
        for i in range(-2, 3):
            bigText = QGraphicsTextItem("", self)
            bigText.setDefaultTextColor(Qt.GlobalColor.white)
            bigText.setFont(self.bigFont)
            smallText = QGraphicsTextItem("", self)
            smallText.setDefaultTextColor(Qt.GlobalColor.white)
            smallText.setFont(self.smallFont)
            variableText = QGraphicsTextItem("", self)
            variableText.setDefaultTextColor(Qt.GlobalColor.white)
            variableText.setFont(self.smallFont)
            self.digits.append({
                "index": i,
                "bigText": bigText,
                "smallText": smallText,
                "variableText": variableText
            })

    def updatePositions(self, altitude):
        mainDigit = self.digits[0]
        bigText = mainDigit["bigText"]
        if isinstance(altitude, numbers.Number):
            step = self.metersPerGraduation * 2
            baseAltitude = (altitude // step) * step

            smallText = mainDigit["smallText"]

            for num in self.digits:
                altitudeValue = baseAltitude + num["index"] * self.metersPerGraduation
                y_local = (altitude - altitudeValue) * self.pxPerMeter
                if altitude<0:
                    y_local=y_local*-1

                variableText = num["variableText"]
                tensDigit = (altitudeValue % 100) // 10 * 10
                variableText.setPlainText(f"{tensDigit:02d}")
                variableText.setPos(self.width*17/16-variableText.boundingRect().width()/2, self.height/2+y_local - variableText.boundingRect().height() / 2)
                variableText.setVisible(True)

            hundredsDigit = (altitude % 1000) // 100
            smallText.setPlainText(str(hundredsDigit))
            smallText.setPos(self.width*19/16-variableText.boundingRect().width()-smallText.boundingRect().width()/2, self.height/2-smallText.boundingRect().height() / 2)
            smallText.setVisible(True)

            thousandsDigit = abs(altitude)//1000
            if altitude>=0:
                bigText.setPlainText(f"{thousandsDigit:02d}")
                bigText.setPos(self.width*19/17-bigText.boundingRect().width()/2-variableText.boundingRect().width()-smallText.boundingRect().width(), self.height/2-bigText.boundingRect().height() / 2)
            else:
                bigText.setPlainText(f"-{thousandsDigit:02d}")
                bigText.setPos(self.width*19/18-bigText.boundingRect().width()/2-variableText.boundingRect().width()-smallText.boundingRect().width(), self.height/2-bigText.boundingRect().height() / 2)
            bigText.setVisible(True)
        else:
            bigText.setPlainText(altitude)
            bigText.setPos(self.width*19/17-bigText.boundingRect().width(), self.height/2-bigText.boundingRect().height() / 2)
            bigText.setVisible(True)

    def boundingRect(self):
        return QRectF(0, self.height/2-self.height/15, self.width*2, self.height*2/15)

    def shape(self):
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path