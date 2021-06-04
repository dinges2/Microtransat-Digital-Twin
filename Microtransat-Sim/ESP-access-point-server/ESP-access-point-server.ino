#include <WiFi.h>
#include <WebServer.h>
#include <ESP32Servo.h>

const char* ssid = "ESP-server";  // Enter SSID here
const char* password = "12345678";  //Enter Password here
int targetRudderAngle = 90;
int targetSailAngle = 90;
int setRudderAngle = 0;
IPAddress local_ip(192,168,1,1);
IPAddress gateway(192,168,1,1);
IPAddress subnet(255,255,255,0);

Servo roerServo;
int roerPin = 13;
//int ledPin = 13;

WebServer server(80);

void setup() {
  Serial.begin(115200);

  WiFi.softAP(ssid, password);
  WiFi.softAPConfig(local_ip, gateway, subnet);
  delay(100);

//  ESP32PWM::allocateTimer(0);
//  ESP32PWM::allocateTimer(1);
//  ESP32PWM::allocateTimer(2);
//  ESP32PWM::allocateTimer(3);
//  roerServo.setPeriodHertz(50);    // standard 50 hz servo
//  roerServo.attach(roerPin, 1000, 2000);
  
  roerServo.attach(roerPin);
  setRudderAngle = map(targetRudderAngle, -90, 90, 0, 180);
  
  server.on("/getTargetSailAngle", getTargetSailAngle);
  server.on("/getTargetRudderAngle", getTargetRudderAngle);
  server.on("/setTargetSailAngle", setTargetSailAngle);
  server.on("setTargetRudderAngle", setTargetRudderAngle);
  server.begin();
  Serial.println("HTTP server started");
}
void loop() {
  server.handleClient();

  roerServo.write(targetRudderAngle);
//  digitalWrite(ledPin, HIGH);
}

void getTargetSailAngle() {
  server.send(200, "text/plain", String(targetSailAngle));
}

void getTargetRudderAngle() {
  server.send(200, "text/plain", String(targetRudderAngle));
}

void setTargetSailAngle(){
  targetSailAngle = server.arg(0).toInt();
  server.send(200, "text/plain", "set sail angle");
}

void setTargetRudderAngle(){
  targetRudderAngle = server.arg(0).toInt();
  server.send(200, "text/plain", "set sail angle");
}
