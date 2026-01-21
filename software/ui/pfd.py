from PyQt6.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QBrush, QPainter

class PrimaryFlightDisplay(QWidget):
    def __init__(self, size=600):
        super().__init__()
        
        self.setMinimumSize(100, 100)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.view = QGraphicsView(self)
        self.scene = QGraphicsScene(0, 0, size, size)
        self.view.setScene(self.scene)
        
        self.view.setFrameShape(QGraphicsView.Shape.NoFrame)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.view.setRenderHints(
            QPainter.RenderHint.Antialiasing | 
            QPainter.RenderHint.SmoothPixmapTransform | 
            QPainter.RenderHint.TextAntialiasing
        )
        self.view.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.SmartViewportUpdate)
        self.view.setCacheMode(QGraphicsView.CacheModeFlag.CacheBackground)
        self.view.setOptimizationFlag(QGraphicsView.OptimizationFlag.DontSavePainterState)

        self.setupMockPFD(size) #Provisoire
        self.setupInstruments()
        self.updateFromData()

    def setupInstruments(self):
        from ui.artificialHorizon.instrument import ArtificialHorizonInstrument
        from ui.altimeter.instrument import AltimeterInstrument
        
        self.artificialHorizon = ArtificialHorizonInstrument()
        self.altimeter = AltimeterInstrument()
        
        self.scene.addItem(self.artificialHorizon)
        self.scene.addItem(self.altimeter)
        
        self.artificialHorizon.setPos(271, 277)
        self.altimeter.setPos(510, 300)

    def showEvent(self, event):
        super().showEvent(event)
        self.updateViewGeometry()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateViewGeometry()

    def updateViewGeometry(self):
        target_w = self.width()
        target_h = self.height()
        side = min(target_w, target_h)
        
        if side > 0:
            x = (target_w - side) // 2
            y = (target_h - side) // 2

            self.view.setGeometry(x, y, side, side)
            self.view.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def updateFromData(self):
        self.artificialHorizon.updatePositions(10, 45)
        self.altimeter.updatePositions(100)

    def setupMockPFD(self, size): #Provisoire
        pixmap = QPixmap("assets/maquette.png")
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(
                size, size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.scene.setBackgroundBrush(QBrush(scaled_pixmap))