//PhotoResistor Pin
int lightPin = 0; //the analog pin the photoresistor is
                  //connected to
                  //the photoresistor is not calibrated to any units so
                  //this is simply a raw sensor value (relative light)
//LED Pin
int ledPin = 9;   //the pin the LED is connected to
                  //we are controlling brightness so
                  //we use one of the PWM (pulse width
                  // modulation pins)
void setup()
{
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT); //sets the led pin to output
}
/*
* loop() � this function will start after setup
* finishes and then repeat
*/
void loop()
{
int lightLevel = analogRead(lightPin); //Read the
                                        // lightlevel

Serial.print(lightLevel);
//adjust the value 0 to 900 to span 0 to 255
//lightLevel = map(lightLevel, 0, 900, 0, 255);

//adjust the value 180 to 610 to span 0 to 255
lightLevel = map(lightLevel, 400, 960, 255, 0);

Serial.print(",");
Serial.println(lightLevel);
delay(50);
lightLevel = constrain(lightLevel, 0, 255);//make sure the
                                           //value is betwween
                                           //0 and 255
analogWrite(ledPin, lightLevel);  //write the value
}
