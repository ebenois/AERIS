import socket
import json


class ESP32Client:
    def __init__(self, port=1234):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.sock.bind(("", port))
        except Exception as e:
            print(f"Erreur Bind UDP: {e}")

        self.sock.settimeout(0.1)
        self.lastPacketId = None

    def read(self):
        try:
            data, _ = self.sock.recvfrom(2048)
            json_data = json.loads(data.decode())
            self.lastPacketId = json_data.get("id")

            return [
                self.lastPacketId,
                json_data.get("pitch", 0),
                json_data.get("roll", 0),
                json_data.get("altitude", 0),
                json_data.get("vario", 0),
                json_data.get("speed", 0),
                json_data.get("heading", 0),
                json_data.get("slip", 0),
            ]
        except:
            return None

    def close(self):
        self.sock.close()
