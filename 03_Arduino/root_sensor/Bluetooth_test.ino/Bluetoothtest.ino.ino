#include <SoftwareSerial.h>

// Création d'un port série logiciel sur les pins 10 (RX) et 11 (TX)
SoftwareSerial bluetooth(10, 11); // RX, TX

void setup() {
  // Démarrer la communication série avec le moniteur série (USB)
  Serial.begin(9600);
  // Démarrer la communication série avec le module Bluetooth
  bluetooth.begin(9600); // Assurez-vous que la vitesse correspond à celle du module

  Serial.println("Bluetooth ready to send data...");
}

void loop() {
  // Définir les variables à envoyer
  int a = 1;
  int b = 2;
  int c = 3;

  // Créer une chaîne de caractères à envoyer
  String message = String(a) + "," + String(b) + "," + String(c) + "\n";

  // Envoyer les données via Bluetooth
  bluetooth.print(message);

  // Afficher également sur le moniteur série pour débogage
  Serial.print("Sent: ");
  Serial.print(message);

  // Attendre 1 seconde avant de renvoyer
  delay(1000);
}
