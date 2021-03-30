int potmeter = A3;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  int sensorValue = analogRead(potmeter);
  //verander de waardes van 0-1023 tot 0-360
  int sensorvalue = map(sensorValue, 0, 1023, 0, 360);
  Serial.print(sensorvalue);
  
  Serial.println("\n");
  delay(50);
}
