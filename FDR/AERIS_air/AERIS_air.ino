// Broches joystick
const int pinX = A0; // Roll (Axe X)
const int pinY = A1; // Pitch (Axe Y)
const int buttonPin = 2;

unsigned int packetId = 0;

// Variables d'état de l'avion
float altitude = 3000.0;   // Altitude initiale (mètres)
float climbRate = 0.0;     // Taux de montée (m/s)
float airspeed = 250.0;    // Vitesse (km/h) - On va la faire varier selon le pitch
float heading = 0.0;       // Cap (0-360)
float slip = 0.0;          // Bille (dérapage)

void setup() {
  Serial.begin(115200);
  pinMode(buttonPin, INPUT_PULLUP);
}

void loop() {
  // 1. Lecture des entrées
  int xValue = analogRead(pinX);  
  int yValue = analogRead(pinY);  
  bool resetPressed = (digitalRead(buttonPin) == LOW);

  if (resetPressed) {
    altitude = 3000.0;
    heading = 0.0;
  }

  // 2. Calcul du Pitch et Roll (Angles en degrés)
  // On mappe vers des angles réalistes (-45° à 45°)
  float roll = map(xValue, 0, 1023, -45, 45);
  float pitch = map(yValue, 0, 1023, -45, 45);

  // 3. Physique du simulateur (Modèle simplifié)
  
  // Le pitch influence le taux de montée (Climb Rate)
  // Si on cabre (pitch positif), on monte.
  climbRate = pitch * 0.5; 
  altitude += climbRate * 0.02; // 0.02 car delay de 20ms
  if (altitude < 0) altitude = 0; // On ne s'écrase pas sous le sol

  // Le roll influence le changement de cap (Heading)
  // Plus on penche, plus on tourne vite.
  float turnRate = roll * 0.1;
  heading += turnRate;
  if (heading >= 360) heading -= 360;
  if (heading < 0) heading += 360;

  // La vitesse (Airspeed) diminue quand on monte et augmente quand on pique
  airspeed = 250.0 - (pitch * 1.5) + (abs(roll) * -0.2);

  // La bille (Slip) réagit à l'inclinaison
  slip = (roll / 45.0) + (0.1 * sin(millis() / 500.0));

  // 4. Envoi du paquet CSV
  // Format : id, roll, pitch, alt, climb, speed, head, slip, button
  Serial.print(packetId);
  Serial.print(",");
  Serial.print(-roll, 1);    // 1 décimale pour la fluidité
  Serial.print(",");
  Serial.print(pitch, 1);
  Serial.print(",");
  Serial.print(altitude, 1);
  Serial.print(",");
  Serial.print(climbRate, 1);
  Serial.print(",");
  Serial.print(airspeed, 1);
  Serial.print(",");
  Serial.print(heading, 1);
  Serial.print(",");
  Serial.print(slip, 2);
  Serial.print(",");
  Serial.println(resetPressed ? 0 : 1);

  packetId = (packetId + 1) % 65536;

  delay(20); // 50 Hz
}