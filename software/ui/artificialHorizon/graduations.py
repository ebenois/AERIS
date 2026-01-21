from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsLineItem, QGraphicsTextItem
from PyQt6.QtGui import QColor, QPen, QFont
from PyQt6.QtCore import Qt

class PitchGraduations(QGraphicsItemGroup):
    def __init__(self, parent=None, width_reference=600):
        super().__init__(parent)
        self.graduations_data = []
        
        pen = QPen(QColor("white"), 3)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        font = QFont("Arial", 18)

        for i in range(-4*12, 4*12 + 1):
            pitch_value = i * 2.5
            
            if i % 4 == 0:
                half_width = width_reference / 12
            elif i % 4 == 2:
                half_width = width_reference / 25
            else:
                half_width = width_reference / 50

            line = QGraphicsLineItem(-half_width, 0, half_width, 0, self)
            line.setPen(pen)

            text_left = None
            text_right = None
            if i % 4 == 0 and i != 0:
                text_left = QGraphicsTextItem(str(int(pitch_value)), self)
                text_left.setDefaultTextColor(Qt.GlobalColor.white)
                text_left.setFont(font)

                text_right = QGraphicsTextItem(str(int(pitch_value)), self)
                text_right.setDefaultTextColor(Qt.GlobalColor.white)
                text_right.setFont(font)

            self.graduations_data.append({
                'line': line,
                'text_left': text_left,
                'text_right': text_right,
                'half_width': half_width,
                'pitch_level': pitch_value
            })

    def updatePositions(self, horizon_y_offset, flipped, pixels_per_degree):
        for grad in self.graduations_data:
            pitch_level = grad['pitch_level']
            
            if not flipped:
                y_local = -pitch_level * pixels_per_degree + horizon_y_offset
            else:
                y_local = pitch_level * pixels_per_degree + horizon_y_offset

            grad['line'].setPos(0, y_local)

            if grad['text_left']:
                t_left = grad['text_left']
                t_right = grad['text_right']
                h_width = grad['half_width']
                
                t_left.setPos(-h_width - 5 - t_left.boundingRect().width(), y_local - t_left.boundingRect().height() / 2)
                t_right.setPos(h_width + 5, y_local - t_right.boundingRect().height() / 2)

