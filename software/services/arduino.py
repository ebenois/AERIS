import serial
import serial.tools.list_ports


class ArduinoReader:
    def __init__(self):
        self.serial = None
        self.port = None
        self.baudrate = 115200

    @staticmethod
    def available_ports():
        return [port.device for port in serial.tools.list_ports.comports()]

    def connect(self, port, baudrate=115200):
        self.disconnect()

        try:
            self.serial = serial.Serial(port, baudrate, timeout=0)
            self.port = port
            self.baudrate = baudrate
            print(f"Arduino connecté sur {port}")
            return True
        except Exception as e:
            print("Erreur Arduino :", e)
            self.serial = None
            return False

    def disconnect(self):
        if self.serial and self.serial.is_open:
            self.serial.close()
            print("Arduino déconnecté")
        self.serial = None

    def is_connected(self):
        return self.serial is not None and self.serial.is_open

    def read(self):
        if not self.is_connected() or self.serial.in_waiting == 0:
            return None

        try:
            line = self.serial.readline().decode(errors="ignore").strip()
            if not line:
                return None

            x, y = map(int, line.split(","))
            return x, y
        except Exception:
            return None