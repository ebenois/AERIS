import serial
import serial.tools.list_ports
import threading
import time

class ArduinoReader:
    def __init__(self):
        self.serial = None
        self.port = None
        self.baudrate = 115200
        
        self.ignoredPackets = 0
        self.ignoredPerSecond = 0

        self._ignoredCounter = 0
        self._lastStatTime = time.time()

        self.thread = None
        self.running = False

        self.latestData = None

        self.lostPackets = 0
        self.ignoredPackets = 0

        self.expectedPacketId = None

    @staticmethod
    def available_ports():
        return [port.device for port in serial.tools.list_ports.comports()]

    def connect(self, port, baudrate=115200):
        self.disconnect()

        try:
            self.serial = serial.Serial(port, baudrate, timeout=0.01)
            self.port = port
            self.baudrate = baudrate

            self.running = True
            self.thread = threading.Thread(target=self.readLoop, daemon=True)
            self.thread.start()

            print(f"Arduino connecté sur {port}")
            return True

        except Exception as e:
            print("Erreur Arduino :", e)
            self.serial = None
            return False
        
    def readLoop(self):
        while self.running:

            try:
                if not self.serial or not self.serial.is_open:
                    continue

                line = self.serial.readline().decode(errors="ignore").strip()

                if not line:
                    continue

                parts = line.split(",")

                if len(parts) != 9:
                    continue

                data = [float(p) for p in parts]
                packetId = int(data[0])

                if self.expectedPacketId is not None:
                    if packetId > self.expectedPacketId:
                        self.lostPackets += packetId - self.expectedPacketId

                self.expectedPacketId = packetId + 1

                if self.latestData is not None:
                    self._ignoredCounter += 1

                self.latestData = data

                # calcul par seconde
                currentTime = time.time()
                if currentTime - self._lastStatTime >= 1.0:
                    self.ignoredPerSecond = self._ignoredCounter
                    self._ignoredCounter = 0
                    self._lastStatTime = currentTime

            except Exception as e:
                print("Erreur série:", e)
            
    def disconnect(self):
        self.running = False

        try:
            if self.thread:
                self.thread.join(timeout=1)
        except:
            pass

        try:
            if self.serial and self.serial.is_open:
                self.serial.close()
                print("Arduino déconnecté")
        except:
            pass

        self.serial = None

    def is_connected(self):
        return self.serial is not None and self.serial.is_open

    def read(self):
        data = self.latestData
        self.latestData = None
        return data