// Définir les broches simulées pour joystick (pour horizon)
const int pinX = A0;
const int pinY = A1;
const int buttonPin = 2;

// Identifiant de paquet
unsigned int packetId = 0;

// Variables simulées pour autres instruments
float altitude = 30000.0;       // en mètres
float climbRate = 0.0;         // m/s
float windSpeed = 200.0;         // m/s
float heading = 0.0;           // en degrés 0-360
float slip = 0.0;              // -1 à 1

void setup() {
  Serial.begin(115200);
  pinMode(buttonPin, INPUT_PULLUP);
}

void loop() {
  // Lire joystick pour pitch/roll
  int xValue = analogRead(pinX);  
  int yValue = analogRead(pinY);  

  int roll = map(xValue, 0, 1023, -360, 360);
  int pitch = map(yValue, 0, 1023, -360, 360);

  // Lire bouton
  int buttonState = digitalRead(buttonPin); // 0 = pressé, 1 = relâché

  // Simuler des variations pour les autres instruments
  altitude += climbRate * 0.02; // incrément selon taux de montée (20ms interval)
  heading += 0.5;                // rotation lente
  if (heading > 360) heading -= 360;
  windSpeed = 250 + 30 * sin(millis() / 10000.0);
  climbRate = 2 * sin(millis() / 5000.0);
  slip = 0.5 * sin(millis() / 3000.0);

  // Envoyer paquet CSV complet
  // Format attendu : packetId,roll,pitch,altitude,climbRate,windSpeed,heading,slip,button
  Serial.print(packetId);
  Serial.print(",");
  Serial.print(-roll);
  Serial.print(",");
  Serial.print(-pitch);
  Serial.print(",");
  Serial.print(altitude);
  Serial.print(",");
  Serial.print(climbRate);
  Serial.print(",");
  Serial.print(windSpeed);
  Serial.print(",");
  Serial.print(heading);
  Serial.print(",");
  Serial.print(slip);
  Serial.print(",");
  Serial.println(buttonState);

  // Incrémenter packetId
  packetId = (packetId + 1) % 65536;

  delay(20); // Correspond à updateIntervalMs = 20ms
}