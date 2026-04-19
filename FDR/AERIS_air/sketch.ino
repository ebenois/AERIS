#include <WiFi.h>
#include <WiFiUdp.h>
#include <Wire.h>
#include <Adafruit_BMP280.h>

const char* ssid = "AERIS_Air";
const char* password = "12345678";

WiFiUDP udp;
const int udpPort = 1234;
IPAddress broadcastIP(192, 168, 4, 255); 

Adafruit_BMP280 bmp;
unsigned long packetId = 0;

void setup() {
    Serial.begin(115200);
    
   if (!bmp.begin(0x76)) { 
        Serial.println("Erreur BMP280");
    }

    WiFi.softAP(ssid, password);
    udp.begin(udpPort);
}

void loop() {
    float pression = bmp.readPressure() / 100.0; // hPa

    packetId++;

    String json = "{";
    json += "\"id\":" + String(packetId) + ",";
    json += "\"pitch\":0,";
    json += "\"roll\":0,";
    json += "\"altitude\":" + String(pression) + ",";
    json += "\"vario\":0,";
    json += "\"speed\":0,";
    json += "\"heading\":0,";
    json += "\"slip\":0";
    json += "}";

    udp.beginPacket(broadcastIP, udpPort);
    udp.print(json);
    udp.endPacket();

    delay(50);
}