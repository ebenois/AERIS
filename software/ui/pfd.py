from PyQt6.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QSizePolicy
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QBrush, QPainter

from ui.artificialHorizon.instrument import ArtificialHorizonInstrument
from ui.altimeter.instrument import AltimeterInstrument
from ui.anemometer.instrument import AnemometerInstrument
from ui.compass.instrument import CompassInstrument
from ui.variometer.instrument import VariometerInstrument

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

        #self.setupMockPFD(size) #Provisoire
        self.setupInstruments()

        test=True
        if test == False:
            self.updateFromData()
        else:
            self.updateTest()

    def updateTest(self):
        pitch, roll, cap, speed, altitude, rise = 10, 10, 230, 250, 38000, 1.5
        self.artificialHorizon.updatePositions(pitch, roll, cap)
        self.altimeter.updatePositions(altitude)
        self.anemometer.updatePositions(speed)
        self.compass.updatePositions(cap)
        self.variometer.updatePositions(rise)

    def setupInstruments(self):
        self.artificialHorizon = ArtificialHorizonInstrument()
        self.altimeter = AltimeterInstrument()
        self.anemometer = AnemometerInstrument()
        self.compass = CompassInstrument()
        self.variometer = VariometerInstrument()

        self.scene.addItem(self.variometer)
        self.scene.addItem(self.artificialHorizon)
        self.scene.addItem(self.altimeter)
        self.scene.addItem(self.anemometer)
        self.scene.addItem(self.compass)
        
        self.variometer.setPos(577, 300)
        self.artificialHorizon.setPos(271, 277)
        self.altimeter.setPos(510, 300)
        self.anemometer.setPos(45, 300)
        self.compass.setPos(271, 715)

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

        roll, pitch = data

        self.last_roll = roll
        self.last_pitch = pitch

        self.artificialHorizon.updatePositions(pitch, roll, roll)
        self.altimeter.updatePositions(pitch)
        self.anemometer.updatePositions(roll)
        self.compass.updatePositions(roll)
        self.variometer.updatePositions(pitch/60)

    def setupMockPFD(self, size): #Provisoire
        pixmap = QPixmap("assets/maquette.png")
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(
                size, size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.scene.setBackgroundBrush(QBrush(scaled_pixmap))