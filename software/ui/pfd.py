from PyQt6.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QSizePolicy
from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtOpenGLWidgets import QOpenGLWidget

from ui.artificialHorizon.instrument import ArtificialHorizonInstrument
from ui.altimeter.instrument import AltimeterInstrument
from ui.anemometer.instrument import AnemometerInstrument
from ui.compass.instrument import CompassInstrument
from ui.variometer.instrument import VariometerInstrument
from ui.slipIndicator.instrument import SlipInstrument
from services.arduino import ArduinoReader


class PrimaryFlightDisplay(QWidget):
    def __init__(self, size=1200):
        super().__init__()
        
        self.setMinimumSize(500, 500)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.view = QGraphicsView(self)
        self.scene = QGraphicsScene(0, 0, size, size)
        self.view.setScene(self.scene)
        
        self.view.setViewport(QOpenGLWidget())

        self.view.setFrameShape(QGraphicsView.Shape.NoFrame)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.view.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        self.view.setCacheMode(QGraphicsView.CacheModeFlag.CacheBackground)
        self.view.setOptimizationFlag(QGraphicsView.OptimizationFlag.DontSavePainterState)

        self.setupInstruments()

        self.audioOutput = QAudioOutput()
        self.audioOutput.setVolume(1)
        self.alertPlayer = QMediaPlayer()
        self.alertPlayer.setAudioOutput(self.audioOutput)
        self.alertPlayer.setSource(QUrl.fromLocalFile("assets/warning.wav"))

        try:
            self.arduino = ArduinoReader(port="COM3", baudrate=115200)
        except Exception as e:
            print(f"Erreur Arduino: {e}")
            self.arduino = None

        self.dataTimer = QTimer()
        self.dataTimer.timeout.connect(self.updateFromArduino)
        self.dataTimer.start(20)

        self.masterTimer = QTimer()
        self.masterTimer.timeout.connect(self.globalHeartbeat)
        self.masterTimer.start(250)
        self.cycleStep = 0

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

        self.instruments = [
            self.artificialHorizon,
            self.altimeter,
            self.anemometer,
            self.compass,
            self.variometer,
            self.slipIndicator
        ]

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateViewGeometry()

    def showEvent(self, event):
        super().showEvent(event)
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

    def updateFromArduino(self):
        if self.arduino is None:
            return

        data = self.arduino.read()
        if data is None:
            return

        x, y = data

        pitch = ""
        roll = ""
        cap = ""
        speed = ""
        altitude = ""
        rise = ""
        slip = ""
        
        self.artificialHorizon.updatePositions(pitch, roll)
        self.altimeter.updatePositions(altitude)
        self.anemometer.updatePositions(speed)
        self.compass.updatePositions(cap)
        self.variometer.updatePositions(rise)
        self.slipIndicator.updatePositions(slip)

    def globalHeartbeat(self):
        self.cycleStep = (self.cycleStep + 1) % 10
        
        isFlashOn = self.cycleStep in [0, 2]
        shouldPlaySound = (self.cycleStep == 0)
        
        anyError = False
        for instr in self.instruments:
            if hasattr(instr, 'isInError') and instr.isInError:
                anyError = True
                break

        if anyError:
            if shouldPlaySound:
                if self.alertPlayer.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
                    self.alertPlayer.stop()
                self.alertPlayer.play()
            
            for instr in self.instruments:
                if hasattr(instr, 'drawAlert'):
                    instr.drawAlert(isFlashOn)
        else:
            for instr in self.instruments:
                if hasattr(instr, 'drawAlert'):
                    instr.drawAlert(False)