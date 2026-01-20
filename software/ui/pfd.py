from PyQt6.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QVBoxLayout
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QPixmap, QBrush

class PrimaryFlightDisplay(QWidget):
    def __init__(self, size=600):
        super().__init__()

        self.view = QGraphicsView()
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, size, size)
        self.view.setScene(self.scene)
        
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.setupMockPFD(size)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.view)

    def setupMockPFD(self, size):
        pixmap = QPixmap("assets/maquette.png").scaled(
            size, size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.scene.setBackgroundBrush(QBrush(pixmap))

    def resizeEvent(self, event):
        super().resizeEvent(event)

        newSize = min(self.width(), self.height())

        if newSize > 0:
            self.view.setFixedSize(newSize, newSize)
            self.view.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)