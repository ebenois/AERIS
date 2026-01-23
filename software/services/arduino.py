import serial

class ArduinoReader:
    def __init__(self, port, baudrate):
        try:
            self.serial = serial.Serial(port, baudrate, timeout=0)
            print(f"Arduino connecté sur {port}")
        except Exception as e:
            print("Erreur Arduino :", e)
            self.serial = None

    def read(self):
        if not self.serial or self.serial.in_waiting == 0:
            return None

        try:
            line = self.serial.readline().decode(errors="ignore").strip()
            if not line:
                return None

            x, y = map(int, line.split(","))
            return x, y

        except Exception:
            return None



