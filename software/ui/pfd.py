from PyQt6.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QSizePolicy
from PyQt6.QtCore import Qt, QTimer, QUrl
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
    updateIntervalMs = 20
    heartbeatIntervalMs = 250

    def __init__(self, size=1200):
        super().__init__()

        self.setMinimumSize(500, 500)
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)
        self.setStyleSheet("background-color: #000000;")

        self.scene = QGraphicsScene(0, 0, size, size, self)
        self.view = QGraphicsView(self.scene, self)
        self.view.setViewport(QOpenGLWidget())
        self.view.setFrameShape(QGraphicsView.Shape.NoFrame)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.view.setViewportUpdateMode(
            QGraphicsView.ViewportUpdateMode.MinimalViewportUpdate
        )
        self.view.setOptimizationFlag(
            QGraphicsView.OptimizationFlag.DontSavePainterState
        )
        self.view.setCacheMode(QGraphicsView.CacheModeFlag.CacheBackground)

        self.setupInstruments()

        self.audioOutput = QAudioOutput(self)
        self.audioOutput.setVolume(1.0)

        self.alertPlayer = QMediaPlayer(self)
        self.alertPlayer.setAudioOutput(self.audioOutput)
        self.alertPlayer.setSource(
            QUrl.fromLocalFile("software/assets/warning.wav")
        )

        try:
            self.arduino = ArduinoReader(port="COM3", baudrate=115200)
        except Exception as e:
            print(f"Erreur Arduino: {e}")
            self.arduino = None

        self.dataTimer = QTimer(self)
        self.dataTimer.timeout.connect(self.updateFromArduino)
        self.dataTimer.start(self.updateIntervalMs)

        self.masterTimer = QTimer(self)
        self.masterTimer.timeout.connect(self.globalHeartbeat)
        self.masterTimer.start(self.heartbeatIntervalMs)

        self.cycleStep = 0
        
        

    def setupInstruments(self):
        self.instruments = [
            ArtificialHorizonInstrument(625, 625),
            AnemometerInstrument(145, 830),
            CompassInstrument(875, 875),
            VariometerInstrument(110, 530),
            AltimeterInstrument(145, 830),
            SlipInstrument(625, 625),
        ]

        positions = [
            (225, 240),   # artificial horizon
            (15, 185),    # anemometer
            (100, 990),   # compass
            (1075, 335),  # variometer
            (915, 185),   # altimeter
            (225, 240),   # slip
        ]

        for instr, pos in zip(self.instruments, positions):
            self.scene.addItem(instr)
            instr.setPos(*pos)

        self.errorCapable = [i for i in self.instruments if hasattr(i, 'isInError')]
        self.alertCapable = [i for i in self.instruments if hasattr(i, 'drawAlert')]

    

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateViewGeometry()

    def showEvent(self, event):
        super().showEvent(event)
        self.updateViewGeometry()

    def updateViewGeometry(self):
        w, h = self.width(), self.height()
        side = min(w, h)

        if side <= 0:
            return

        x = (w - side) // 2
        y = (h - side) // 2

        self.view.setGeometry(x, y, side, side)
        self.view.fitInView(
            self.scene.sceneRect(),
            Qt.AspectRatioMode.KeepAspectRatio
        )

    

    def updateFromArduino(self):
        if not self.arduino:
            return

        data = self.arduino.read()
        if not data:
            return

        for instr in self.instruments:
            instr.updatePositions(data)

    

    def globalHeartbeat(self):
        self.cycleStep = (self.cycleStep + 1) % 10

        flashOn = self.cycleStep in (0, 2)
        playSound = self.cycleStep == 0

        anyError = any(i.isInError for i in self.errorCapable)

        if anyError:
            if playSound:
                self.alertPlayer.play()

            for instr in self.alertCapable:
                instr.drawAlert(flashOn)
        else:
            for instr in self.alertCapable:
                instr.drawAlert(False)