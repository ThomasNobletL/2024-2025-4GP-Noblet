// Inclusion de la librairie 
#include <LiquidCrystal.h> // Dimension de l'afficheur 
const int numRows = 2; 
const int numCols = 16; // Initialisation de la librarie avec le nbre de pins d'interface // 4 bit de données dans notre cas.
/* Le montage:  Afficheur LCD  
* LCD RS     - pin 2  
* LCD Enable - pin 3  
* LCD D4     - pin 4  
* LCD D5     - pin 5 
* LCD D6     - pin 6 
* LCD D7     - pin 7 
* LCD R/W    - GND 
* LCD Vo contrast- potentiom�tre 10K (entre Gnd et +5V) 
*/
LiquidCrystal lcd(2,3,4,5,6,7); 

void setup() {   

Serial.begin(9600);   // Bouton changer th�me  
lcd.begin(numCols,numRows);      //--- Message de bienvenue -----  
lcd.print( "demo LCD" );   // placer curseur sur ligne 2  
lcd.setCursor(0,1); // col, row  
lcd.print( "Hello!" );   // clignotement curseur plein  
lcd.blink();
}

void loop()
{



 } 
