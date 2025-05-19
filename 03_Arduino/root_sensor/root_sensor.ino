#include <SPI.h>
#include <LiquidCrystal_I2C.h>
#include <SoftwareSerial.h>

//Definition du BaudRate
#define baudrate 9600

//Definitions des pins
#define Rx 2 //Vers le TX du HCO5
#define Tx 3 //Vers le RX du HCO5

#define OutRaw A0 // Sortie directe depuis le capteur graphite
#define OutAmp A1 // Sortie amplifiée par le LTC1050 du capteur graphite

#define MOSI 11 // entrée de commandes du MCP41050
#define CS 12 // Chip select du MCP41050
#define SCK 13 // serial Clock du MCP41050

//Definition des valeurs fixes

#define Rab 50000 // Resistance MAX du MCP41050
#define Rw 125 //Resistance Interne du MCP41050


byte resistanceValue = 128;

String inputBuffer = ""; // Pour stocker les commandes Bluetooth

SoftwareSerial BTserial(Rx, Tx);

void setup() {
  Serial.begin(baudrate);       // Moniteur série USB
  BTserial.begin(baudrate);     // Communication Bluetooth HC-05

  pinMode(CS, OUTPUT);
  digitalWrite(CS, HIGH);

  SPI.begin();
  setResistance(resistanceValue);
}

void loop() {
  // Lire les tensions A0 et A1 
  int valA0 = analogRead(OutRaw);
  int valA1 = analogRead(OutAmp);

  // Lecture des données entrantes via Bluetooth 
  while (BTserial.available()) {
    char c = BTserial.read();

    if (c == '\n' || c == '\r') {
      processCommand(inputBuffer);
      inputBuffer = "";
    } else {
      inputBuffer += c;
    }
  }

  // Envoi des données sur Bluetooth
  BTserial.print(valA0);
  BTserial.print(" ");
  BTserial.println(valA1);

  delay(200);
}

void setResistance(byte value) {
  digitalWrite(CS, LOW);  
  SPI.transfer(0x11);  
  SPI.transfer(value);
  digitalWrite(CS, HIGH);
}

void processCommand(String cmd) {
  cmd.trim();
  cmd.toUpperCase();

  if (cmd.startsWith("SET")) {
    int val = cmd.substring(3).toInt();
    if (val >= 0 && val <= 255) {    //Vérification que la valeur envoyée est dans la plage
      resistanceValue = val;
      setResistance(resistanceValue);
      Serial.print("Resistance set to ");
      Serial.println(resistanceValue);
    } else {
      serial.print("Value out of range (0-255)");
    }

  } else {
    serial.print("Unknown command"); //Affichage de l'erreur sur le moniteur série
    serial.println(String cmd)
  }
}
