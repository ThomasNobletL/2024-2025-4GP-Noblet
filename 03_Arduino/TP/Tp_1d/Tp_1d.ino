int ledPin =  13;    // LED connected to digital pin 13
int incomingByte = 0;   //serial char
 
// The setup() method runs once, when the sketch starts
 
void setup()   {
  // opens serial port, sets data rate to 9600 bps
  Serial.begin(9600);
  // initialize the digital pin as an output:
  pinMode(ledPin, OUTPUT);    
  digitalWrite(ledPin, LOW);
}
 
// the loop() method runs over and over again,
// as long as the Arduino has power
 
void loop()                    
{
  if (Serial.available() > 0) {
	// read the incoming byte:
	incomingByte = Serial.read();
        
        if (incomingByte == 'y')
        {
	  digitalWrite(ledPin, HIGH);    // set the LED ON
        }
        else if (incomingByte == 'n')
        {
          digitalWrite(ledPin, LOW);    // set the LED off
        }
 }
 delay(250);                  // wait for a second
}
