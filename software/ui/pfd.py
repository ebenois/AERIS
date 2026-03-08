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
import time


class PrimaryFlightDisplay(QWidget):
    def __init__(self, size=1200):
        super().__init__()

        self.updateIntervalMs = 10
        self.heartbeatIntervalMs = 250

        self.lastDataTime = time.time()
        self.isConnected = False
        self.connectionTimeout = 0.5
        self.flashState = False
        self.cycleStep = 0

        self.consecutivePacketLoss = 0
        self.maxAllowedLoss = 5
        self.dataIntegrityError = False

        self.arduino = None

        self.setMinimumSize(500, 500)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
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
        self.alertPlayer.setSource(QUrl.fromLocalFile("software/assets/warning.wav"))

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
            (225, 240),  # artificial horizon
            (15, 185),   # anemometer
            (100, 990),  # compass
            (1075, 335), # variometer
            (915, 185),  # altimeter
            (225, 240),  # slip
        ]

        for instr, pos in zip(self.instruments, positions):
            self.scene.addItem(instr)
            instr.setPos(*pos)

        self.alertInstruments = [i for i in self.instruments if hasattr(i, "drawAlert")]
        self.errorCapable = [i for i in self.instruments if hasattr(i, "isInError")]


    def globalHeartbeat(self):
        currentTime = time.time()

        if currentTime - self.lastDataTime > self.connectionTimeout:
            if self.isConnected:
                self.isConnected = False
                if self.window():
                    self.window().updateArduinoStatus(False)
            for instr in self.errorCapable:
                instr.isInError = True

        anyError = any(getattr(instr, "isInError", False) for instr in self.errorCapable)
        anyCritical = any(getattr(instr, "isCritical", False) for instr in self.errorCapable)

        self.flashState = self.cycleStep in (0, 2)

        if self.cycleStep in (0, 2) and (anyError or anyCritical):
            self.alertPlayer.play()

        for instr in self.alertInstruments:
            if getattr(instr, "isInError", False) or getattr(instr, "isCritical", False):
                instr.drawAlert(self.flashState)
            else:
                instr.drawAlert(False)

        highMentalLoad = any(getattr(instr, "isCritical", False) for instr in self.instruments)
        
        horizon = self.instruments[0]
        anemometer = self.instruments[1]
        compas = self.instruments[2]
        variometer = self.instruments[3]
        altimeter = self.instruments[4]
        slip = self.instruments[5]

        for instr in self.instruments:
            instr.drawLess(False)

        if highMentalLoad:
            if anemometer.isCritical:
                compas.drawLess(True)
                variometer.drawLess(True)
            
            if horizon.isCritical:
                compas.drawLess(True)
                variometer.drawLess(True)
                slip.drawLess(True)
                altimeter.drawLess(True)
            
            if altimeter.isCritical or variometer.isCritical:
                compas.drawLess(True)
                slip.drawLess(True)
                
        self.cycleStep = (self.cycleStep + 1) % 5

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
        self.view.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def updateFromArduino(self):
        if not self.arduino:
            return

        data = self.arduino.read()
        currentTime = time.time()

        if data is None:
            if currentTime - self.lastDataTime > self.connectionTimeout:
                if self.isConnected:
                    self.isConnected = False
                    self.window().updateArduinoStatus(False)
                    print("⚠ Connexion perdue avec l'Arduino")

                for instr in self.errorCapable:
                    instr.isInError = True
            return

        self.lastDataTime = currentTime

        if not self.isConnected:
            self.isConnected = True
            self.window().updateArduinoStatus(True)
            print("Connexion rétablie")

        # data = [id, roll, pitch, alt, climb, speed, head, slip, btn]
        try:
            packetId = int(data[0])
        except (ValueError, IndexError, TypeError):
            return

        print(
                f"lost={self.arduino.lostPackets} ignored/s={self.arduino.ignoredPerSecond}"
            )

        self.dataIntegrityError = self.consecutivePacketLoss > self.maxAllowedLoss

        if not self.dataIntegrityError:
            self.updatePositions(data)
        else:
            for instr in self.errorCapable:
                instr.isInError = True

    def updatePositions(
        self, data
    ):  # data = [id, roll, pitch, alt, climb, speed, head, slip, btn]
        self.instruments[0].updatePositions(data[1], data[2])  # Horizon (roll, pitch)
        self.instruments[1].updatePositions(data[5])  # Vitesse (airspeed)
        self.instruments[2].updatePositions(data[6])  # Cap (heading)
        self.instruments[3].updatePositions(data[4])  # Variomètre (climbRate)
        self.instruments[4].updatePositions(
            data[2], data[3], data[5]
        )  # Altimètre (altitude)
        self.instruments[5].updatePositions(data[7])  # Bille (slip)

    def setArduino(self, arduino):
        self.arduino = arduino
