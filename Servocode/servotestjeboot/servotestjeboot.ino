// zoomkat 10-22-11 serial servo test
// type servo position 0 to 180 in serial monitor
// or for writeMicroseconds, use a value like 1500
// for IDE 0022 and later
// Powering a servo from the arduino usually *DOES NOT WORK*.

// Rudder servo works as intended
// Rudder has double headers on extension cord
// Sail winch values range from 130-180 degrees, could be related to the physical position of the servo.
// Map to a variable

String readString;
#include <Servo.h> 
Servo myservo;  // create servo object to control a servo 

void setup() {
  Serial.begin(9600);
  myservo.writeMicroseconds(1500); //set initial servo position if desired
  myservo.attach(2, 1000, 2000);  //the pin for the servo control, and range if desired
  Serial.println("servo-test-22-dual-input"); // so I can keep track of what is loaded
}

void loop() {
//  while (Serial.available()) {
//    char c = Serial.read();  //gets one byte from serial buffer
//    readString += c; //makes the string readString
//    delay(2);  //slow looping to allow buffer to fill with next character
//  }
//
//  if (readString.length() >0) {
//    Serial.println(readString);  //so you can see the captured string 
//    int n = readString.toInt();  //convert readString into a number
//
//    // auto select appropriate value, copied from someone elses code.
//    if(n >= 500)
//    {
//      Serial.print("writing Microseconds: ");
//      Serial.println(n);
//      myservo.writeMicroseconds(n);
//    }
//    else
//    {   
//      Serial.print("writing Angle: ");
//      Serial.println(n);
//      myservo.write(n);
//    }
//    Serial.print("Last servo command position: ");    
//    Serial.println(myservo.read());
//    readString=""; //empty for next input
//  } 

    for (int i = 0; i < 100; i++){
      delay(100);
      myservo.write(i);
        if (i > 98){
          i = 0;
      }
    }
}
