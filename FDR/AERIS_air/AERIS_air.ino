// Broches joystick
const int pinX = A0; // Roll (Axe X)
const int pinY = A1; // Pitch (Axe Y)
const int buttonPin = 2;

unsigned int packetId = 0;

// Variables d'état de l'avion
float altitude = 3000.0;   // Altitude initiale (feet)
float climbRate = 0.0;     // Taux de montée (feet/knot)
float airspeed = 250.0;    // Vitesse (knot)
float heading = 0.0;       // Cap (0-360)
float slip = 0.0;          // Bille (dérapage)
float knotPerFeet = 1.68781;

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
    airspeed = 250;
  }

  // 2. Calcul du Pitch et Roll (Angles en degrés)
  // On mappe vers des angles réalistes (-45° à 45°)
  float roll = map(xValue, 0, 1023, -45, 45);
  float pitch = map(yValue, 0, 1023, -45, 45);

  // 3. Physique du simulateur (Modèle simplifié)
  
  // Le pitch influence le taux de montée (Climb Rate)
  // Si on cabre (pitch positif), on monte.
  float pitchRad = pitch * PI / 180.0;
  float rollRad  = roll  * PI / 180.0;

  // Montée (vertical speed)
  climbRate = sin(pitchRad) * airspeed * 101.27; // knots → ft/min approx
  altitude += climbRate * 0.000333; // conversion ft/min vers 20ms

  if (altitude < -100) altitude = 0;

  // Taux de virage réaliste simplifié
  float turnRate = tan(rollRad) * (airspeed / 100.0);
  heading += turnRate;

  if (heading >= 360) heading -= 360;
  if (heading < 0) heading += 360;

  // Vitesse simplifiée
  airspeed += (-sin(pitchRad) * 2.0);
  airspeed -= abs(rollRad) * 0.5;

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