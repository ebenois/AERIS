// Broches joystick
const int pinX = A0; // Axe X (commande roulis)
const int pinY = A1; // Axe Y (commande tangage)
const int buttonPin = 2;

unsigned int packetId = 0;

// Etat de l'avion
float altitude = 3000.0;
float climbRate = 0.0;
float airspeed = 250.0;
float heading = 0.0;
float slip = 0.0;

// Attitude avion
float pitch = 0.0;
float roll  = 0.0;

// vitesses de rotation
float pitchRate = 0.0;
float rollRate  = 0.0;

void setup() {
  Serial.begin(115200);
  pinMode(buttonPin, INPUT_PULLUP);
}

void loop() {

  // Lecture joystick
  int xValue = analogRead(pinX);
  int yValue = analogRead(pinY);
  bool resetPressed = (digitalRead(buttonPin) == LOW);

  if (resetPressed) {
    altitude = 3000.0;
    heading = 0.0;
    airspeed = 250;
    pitch = 0;
    roll = 0;
  }

  // Centre joystick
  float joyX = (xValue - 512) / 512.0;
  float joyY = (yValue - 512) / 512.0;

  // petite zone morte
  if (abs(joyX) < 0.05) joyX = 0;
  if (abs(joyY) < 0.05) joyY = 0;

  // Le manche commande la VITESSE de rotation
  float targetRollRate  = joyX * 120.0;  // deg/sec
  float targetPitchRate = joyY * 90.0;   // deg/sec

  // Inertie du manche
  rollRate  += (targetRollRate - rollRate) * 0.1;
  pitchRate += (targetPitchRate - pitchRate) * 0.1;

  // Mise à jour attitude avion
  roll  += rollRate * 0.02;
  pitch += pitchRate * 0.02;

  // Limites réalistes
  if (roll > 60) roll = 60;
  if (roll < -60) roll = -60;
  if (pitch > 45) pitch = 45;
  if (pitch < -45) pitch = -45;

  float pitchRad = pitch * PI / 180.0;
  float rollRad  = roll  * PI / 180.0;

  // Montée
  climbRate = sin(pitchRad) * airspeed * 101.27;
  altitude += climbRate * 0.000333;

  if (altitude < 0) altitude = 0;

  // Virage
  float turnRate = tan(rollRad) * (airspeed / 100.0);
  heading -= turnRate;

  if (heading >= 360) heading -= 360;
  if (heading < 0) heading += 360;

  // vitesse simplifiée
  airspeed += (-sin(pitchRad) * 2.0);
  airspeed -= abs(rollRad) * 0.5;

  // bille
  slip = (roll / 45.0) + (0.1 * sin(millis() / 500.0));

  // Envoi CSV
  Serial.print(packetId);
  Serial.print(",");
  Serial.print(-roll, 1);
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

  delay(20);
}