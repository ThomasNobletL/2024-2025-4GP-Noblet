#include <Servo.h>

#define PIN_SERVO 11
#define PIN_FLEX_SENSOR A0

Servo myservo;

int pos = 0;
int pos_max = 150;
int pos_min = 20;
 
void setup() {
  Serial.begin(9600);  
  myservo.attach(PIN_SERVO);
}

int measure(){
  Serial.println(analogRead(PIN_FLEX_SENSOR));
  delay(50); 
  return analogRead(PIN_FLEX_SENSOR);
}

void loop() {


  int valeur = measure();
  int servo_valeur = map(valeur, 700, 900, 0, 255);
  myservo.write(servo_valeur);           
}


