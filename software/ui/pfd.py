from PyQt6.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QSizePolicy
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QBrush, QPainter

from ui.artificialHorizon.instrument import ArtificialHorizonInstrument
from ui.altimeter.instrument import AltimeterInstrument
from ui.anemometer.instrument import AnemometerInstrument
from ui.compass.instrument import CompassInstrument
from ui.variometer.instrument import VariometerInstrument
from ui.slipIndicator.instrument import SlipInstrument

class PrimaryFlightDisplay(QWidget):
    def __init__(self, size=1200):
        super().__init__()
        
        self.setMinimumSize(500, 500)
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

        #self.setupMockPFD(size) #Provisoire
        self.setupInstruments()

        self.updateFromData()

    def setupInstruments(self):
        self.artificialHorizon = ArtificialHorizonInstrument(625,625)
        self.altimeter = AltimeterInstrument(145,830)
        self.anemometer = AnemometerInstrument(145,830)
        self.compass = CompassInstrument(875,875)
        self.variometer = VariometerInstrument(110,530)
        self.slipIndicator = SlipInstrument(625,625)

        self.scene.addItem(self.variometer)
        self.scene.addItem(self.artificialHorizon)
        self.scene.addItem(self.altimeter)
        self.scene.addItem(self.anemometer)
        self.scene.addItem(self.compass)
        self.scene.addItem(self.slipIndicator)
        
        self.variometer.setPos(1075, 335)
        self.artificialHorizon.setPos(225, 240)
        self.altimeter.setPos(915, 185)
        self.anemometer.setPos(15, 185)
        self.compass.setPos(100, 990)
        self.slipIndicator.setPos(225, 240)

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
        from services.arduino import ArduinoReader
        self.arduino = ArduinoReader(port="COM3", baudrate=115200)

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateFromArduino)
        self.timer.start(20)

    def updateFromArduino(self):
        data = self.arduino.read()

        if data is None:
            return

        x, y = data

        instrument = 0

        pitch, roll, cap, speed, altitude, rise, slip = 0, 0, 230, 250, 38000, 1.5, 20

        if instrument == 1:
            self.artificialHorizon.updatePositions(y, x)
        else:
            self.artificialHorizon.updatePositions(pitch, roll)

        if instrument == 2:
            self.altimeter.updatePositions(y+38000)
        else:
            self.altimeter.updatePositions(altitude)

        if instrument == 3:
            self.anemometer.updatePositions(y)
        else:
            self.anemometer.updatePositions(speed)

        if instrument == 4:
            self.compass.updatePositions(x%360)
        else:
            self.compass.updatePositions(cap)

        if instrument == 5:
            self.variometer.updatePositions(y/60)
        else:
            self.variometer.updatePositions(rise)

        if instrument == 6:
            self.slipIndicator.updatePositions(x/6)
        else:
            self.slipIndicator.updatePositions(slip)

    def setupMockPFD(self, size): #Provisoire
        path = "assets/maquette.png"
        pixmap = QPixmap("assets/maquette.png")
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(
                size, size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.scene.setBackgroundBrush(QBrush(scaled_pixmap))