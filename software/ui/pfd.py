from PyQt6.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QVBoxLayout
from PyQt6.QtCore import QSize

class PrimaryFlightDisplay(QWidget):
    def __init__(self, size=600):
        super().__init__()

        self.view = QGraphicsView()
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(-size/2, -size/2, size, size)
        self.view.setScene(self.scene)
        self.view.setMinimumSize(QSize(size, size))

        layout = QVBoxLayout(self)
        layout.addWidget(self.view)
