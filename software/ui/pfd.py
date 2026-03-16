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
import math


class PrimaryFlightDisplay(QWidget):

    UPDATE_INTERVAL = 10
    HEARTBEAT_INTERVAL = 30
    CONNECTION_TIMEOUT = 0.5
    MAX_PULSE_STEPS = 50
    PULSE_TIME = 15

    def __init__(self, size=1200):
        super().__init__()

        self.lastDataTime = time.time()
        self.isConnected = False
        self.pulseStep = 0

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

        self.setupAudio()
        self.setupTimers()

    def setupTimers(self):
        self.dataTimer = QTimer(self)
        self.dataTimer.timeout.connect(self.updateFromArduino)
        self.dataTimer.start(self.UPDATE_INTERVAL)

        self.masterTimer = QTimer(self)
        self.masterTimer.timeout.connect(self.globalHeartbeat)
        self.masterTimer.start(self.HEARTBEAT_INTERVAL)

    def setupAudio(self):
        self.audioOutput = QAudioOutput(self)
        self.audioOutput.setVolume(1.0)

        self.alertPlayer = QMediaPlayer(self)
        self.alertPlayer.setAudioOutput(self.audioOutput)
        self.alertPlayer.setSource(QUrl.fromLocalFile("software/assets/warning.wav"))

    def setupInstruments(self):

        self.horizon = ArtificialHorizonInstrument(625, 625)
        self.anemometer = AnemometerInstrument(145, 830)
        self.compass = CompassInstrument(875, 875)
        self.variometer = VariometerInstrument(110, 530)
        self.altimeter = AltimeterInstrument(145, 830)
        self.slip = SlipInstrument(625, 625)

        self.instruments = [
            self.horizon,
            self.anemometer,
            self.compass,
            self.variometer,
            self.altimeter,
            self.slip,
        ]

        positions = [
            (225, 240),
            (15, 185),
            (100, 990),
            (1075, 335),
            (915, 185),
            (225, 240),
        ]

        for instr, pos in zip(self.instruments, positions):
            self.scene.addItem(instr)
            instr.setPos(*pos)

        self.alertInstruments = [i for i in self.instruments if hasattr(i, "drawAlert")]
        self.errorCapable = [i for i in self.instruments if hasattr(i, "isInError")]

    def globalHeartbeat(self):

        now = time.time()

        if now - self.lastDataTime > self.CONNECTION_TIMEOUT:
            if self.isConnected:
                self.isConnected = False
                if self.window():
                    self.window().updateArduinoStatus(False)

            for instr in self.errorCapable:
                instr.isInError = True

        anyError = any(i.isInError for i in self.errorCapable)
        anyCritical = any(getattr(i, "isCritical", False) for i in self.errorCapable)

        flashOpacity = 0

        if anyError or anyCritical:

            self.pulseStep = (self.pulseStep + 1) % self.MAX_PULSE_STEPS

            if self.pulseStep < self.PULSE_TIME:

                phase = (self.pulseStep / self.PULSE_TIME) * math.pi
                flashOpacity = 0.35 + 0.65 * math.sin(phase)

                if self.pulseStep == 0:
                    self.alertPlayer.stop()
                    self.alertPlayer.play()

            elif self.pulseStep < self.PULSE_TIME * 2:

                phase = ((self.pulseStep - self.PULSE_TIME) / self.PULSE_TIME) * math.pi
                flashOpacity = 0.35 + 0.65 * math.sin(phase)

        else:
            self.pulseStep = 0

        self.drawAlert(flashOpacity)

        if anyCritical or anyError:
            self.drawLess(True)
        else:
            self.drawLess(False)

    def drawLess(self, isOn):

        for instr in self.instruments:
            instr.drawLess(False)

        if not isOn:
            return

        def isProblem(instr):
            return getattr(instr, "isCritical", False) or getattr(
                instr, "isInError", False
            )

        if isProblem(self.anemometer):
            if not isProblem(self.compass):
                self.compass.drawLess(True)
            if not isProblem(self.variometer):
                self.variometer.drawLess(True)

        if isProblem(self.altimeter) or isProblem(self.variometer):
            if not isProblem(self.compass):
                self.compass.drawLess(True)
            if not isProblem(self.slip):
                self.slip.drawLess(True)

        if isProblem(self.horizon):
            if not isProblem(self.compass):
                self.compass.drawLess(True)
            if not isProblem(self.variometer):
                self.variometer.drawLess(True)
            if not isProblem(self.slip):
                self.slip.drawLess(True)
            if not isProblem(self.altimeter):
                self.altimeter.drawLess(True)

    def drawAlert(self, flashOpacity):
        secondaryFlashOpacity = 0.10
        if self.horizon.isCritical:
            for instr in self.alertInstruments:
                if instr == self.horizon:
                    instr.drawAlert(flashOpacity)
                else:
                    instr.drawAlert(secondaryFlashOpacity)
        elif self.anemometer.isCritical:
            for instr in self.alertInstruments:
                if instr == self.anemometer:
                    instr.drawAlert(flashOpacity)
                else:
                    instr.drawAlert(secondaryFlashOpacity)
        elif self.altimeter.isCritical:
            for instr in self.alertInstruments:
                if instr == self.altimeter:
                    instr.drawAlert(flashOpacity)
                else:
                    instr.drawAlert(secondaryFlashOpacity)
        elif self.variometer.isCritical:
            for instr in self.alertInstruments:
                if instr == self.variometer:
                    instr.drawAlert(flashOpacity)
                else:
                    instr.drawAlert(secondaryFlashOpacity)
        elif self.slip.isCritical:
            for instr in self.alertInstruments:
                if instr == self.slip:
                    instr.drawAlert(flashOpacity)
                else:
                    instr.drawAlert(secondaryFlashOpacity)
        else:
            for instr in self.alertInstruments:
                instr.drawAlert(flashOpacity)
        return

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateViewGeometry()

    def showEvent(self, event):
        super().showEvent(event)
        self.updateViewGeometry()

    def updateViewGeometry(self):

        side = min(self.width(), self.height())
        if side <= 0:
            return

        x = (self.width() - side) // 2
        y = (self.height() - side) // 2

        self.view.setGeometry(x, y, side, side)
        self.view.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def updateFromArduino(self):

        if not self.arduino:
            return

        data = self.arduino.read()
        now = time.time()

        if data is None:
            if now - self.lastDataTime > self.CONNECTION_TIMEOUT and self.isConnected:

                self.isConnected = False
                self.window().updateArduinoStatus(False)

                for instr in self.errorCapable:
                    instr.isInError = True

            return

        self.lastDataTime = now

        if not self.isConnected:
            self.isConnected = True
            self.window().updateArduinoStatus(True)

        try:
            int(data[0])
        except (ValueError, IndexError, TypeError):
            return

        self.dataIntegrityError = self.consecutivePacketLoss > self.maxAllowedLoss

        if self.dataIntegrityError:
            for instr in self.errorCapable:
                instr.isInError = True
            return

        self.updatePositions(data)

    def updatePositions(self, data):

        self.horizon.updatePositions(data[1], data[2])
        self.anemometer.updatePositions(data[5])
        self.compass.updatePositions(data[6])
        self.variometer.updatePositions(data[4])
        self.altimeter.updatePositions(data[2], data[3], data[5])
        self.slip.updatePositions(data[7])

    def setArduino(self, arduino):
        self.arduino = arduino
