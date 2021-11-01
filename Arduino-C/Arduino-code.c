/*
 * Rui Santos 
 * Complete Project Details https://randomnerdtutorials.com
 * completed by biero-el-corridor for the LoRa-GPS-Tracker Project
 */
#include <SoftwareSerial.h>
#include "TinyGPS++.h"
#include <NMEAGPS.h>

SoftwareSerial serGPS(4, 3); //rx, tx
SoftwareSerial serLoRa(7, 8);

char machaine[60];
float RecupLatFloat; 
char RecupLatChar[15];
float RecupLongFloat; 
char RecupLongChar[15];

NMEAGPS gps; // the parser
gps_fix fix; // the struct with all the parsed values
// The TinyGPS++ object
//TinyGPSPlus gps;

void setup() {
  serLoRa.begin(9600);
  serGPS.begin(9600); // GPS serial
  //faire atentions le placmeent des begin et important
  Serial.begin(9600); // USB serial
}

void loop() {
  if (gps.available( serGPS )) {
    delay(1000);
    fix = gps.read();  
    Serial.println("Latitude:");
    Serial.println( fix.latitude(), 8);
    RecupLatFloat = fix.latitude();
    //Serial.println(RecupLatFloat);
    //on selectionne 12 cap celas peut aller jusqua -180.0000000 = tab[12]
    dtostrf(RecupLatFloat, 12, 7,RecupLatChar);
    
    Serial.println("Longitude:");
    Serial.println( fix.longitude(), 8);
    RecupLongFloat = fix.longitude() ;
    dtostrf(RecupLongFloat, 12, 7,RecupLongChar);


    sprintf(machaine, "AT+SEND=1,25,%s,%s\r\n",RecupLatChar , RecupLongChar );
    serLoRa.begin(9600);
    
    delay(1000);
    serLoRa.println(machaine);
    //le truc se print bien mais pas au bon endroit 
    //Serial.println(machaine);
    delay(1000);
    serLoRa.end();
    serGPS.begin(9600);

  }
}