int pinMoteur = 9; // pin controlant le moteur (PWM pin)

void setup(){
  //En PWM il ne faut pas assigner la pin en output 
}

void loop(){
   MoteurVitessePWM();
   MoteurAccelerationPWM(); 
}

// Controle de la vitesse du moteur en controlant
//   le pourcentage du cycle de service PWM sur 
//   la pin 9 (de 0 &agrave; 255 pour 
//   le % du cycle de service ).
//
void MoteurVitessePWM(){
  int vitesse1 = int(255) / 3; // High 33% du cycle
  int vitesse2 = int(255) / 2; // High 50% du cycle
  int vitesse3 = 2 * 255 / 3;
  int vitesse4 = (int)255;     // High 100% du cycle
  
  analogWrite( pinMoteur, vitesse1 );
  delay( 1000 );
  analogWrite( pinMoteur, vitesse2 );
  delay( 1000 );
  analogWrite( pinMoteur, vitesse3 );
  delay( 1000 ); 
  analogWrite( pinMoteur, vitesse4 );
  delay( 1000 );
  analogWrite( pinMoteur, vitesse3 );
  delay( 1000 );
  analogWrite( pinMoteur, vitesse2 );
  delay( 1000 );
  analogWrite( pinMoteur, vitesse1 );
  delay( 1000 );
  analogWrite( pinMoteur, LOW );
}

// Controle plus fin de l&#039;acceleration du moteur via PWM.
// NB: Selon la qualit&eacute; du moteur, celui-ci peut avoir du mal &agrave; d&eacute;coller 
//     lorsque le % du cycle de service est assez bas.
//     Un option est d&#039;envoyer une impulsion pour d&eacute;marrer/d&eacute;coller le moteur.
void MoteurAccelerationPWM(){
  // Impulsion de d&eacute;marrage (75%)
  //analogWrite( pinMoteur, 191 );
  //delay(50);
  
  // Acceleration
  for( int i = 30; i<= 255; i++ ){
    analogWrite( pinMoteur, i );
    delay(50); // delay pour avoir un progression
  }
  
  // pause de 2 secondes a plein r&eacute;gime
  delay( 2000 );  
  
  // Deceleration
  for( int i = 255; i>=0; i-- ){
    analogWrite( pinMoteur, i );
    delay(50); // delay pour avoir un progression
  }
}
 