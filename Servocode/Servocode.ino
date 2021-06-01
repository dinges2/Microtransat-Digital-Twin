// Include the Servo library 
#include <Servo.h>

int zeilPin = 2;
int roerPin = 3;
Servo zeilServo;
Servo roerServo;

int incomingByte;
int test;
String data;
int zeil;
int roer;

void verwerkData(String get){
  zeil = get.substring(0, 3).toInt();
  roer = get.substring(3).toInt();
}

void setup() {
  Serial.begin(9600);
  zeilServo.attach(zeilPin);
  roerServo.attach(roerPin);
}

void loop(){     
  
    while(Serial.available()){
      incomingByte = Serial.read();
      if(incomingByte == ' ' || incomingByte == '\r' || incomingByte == '\n'){
        verwerkData(data);
//        delay(500);
        data = "";
      }
      else{
        test = incomingByte - '0';
        data += test;
      }
    }
    zeilServo.write(zeil);
    roerServo.write(roer);
//    Serial.print("Zeil: ");
//    Serial.println(zeil);
//    Serial.print("Roer: ");
//    Serial.println(roer);
}
