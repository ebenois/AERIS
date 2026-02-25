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
            self.serial = serial.Serial(port, baudrate, timeout=0.1)
            self.port = port
            self.baudrate = baudrate
            print(f"Arduino connecté sur {port}")
            return True
        except Exception as e:
            print("Erreur Arduino :", e)
            self.serial = None
            return False

    def disconnect(self):
        try:
            if self.serial and self.serial.is_open:
                self.serial.close()
                print("Arduino déconnecté")
        except Exception:
            pass
        self.serial = None

    def is_connected(self):
        return self.serial is not None and self.serial.is_open

    def read(self):
        try:
            if not self.is_connected():
                return None

            if self.serial.in_waiting == 0:
                return None

            line = self.serial.readline().decode(errors="ignore").strip()
            if not line:
                return None

            parts = line.split(",")
            if len(parts) != 9:
                print(f"⚠ Paquet invalide (attendu 9 valeurs) : {line}")
                return None

            # Convertir en float
            data = [float(p) for p in parts]
            return data

        except Exception as e:
            print(f"⚠ Erreur série: {e}")
            self.disconnect()
            return None