from arduinoInputData import *
import serial
import sys

class ArduinoOutputData:
    def __init__(self):
        self.port = 'COM6'
        self.arduino = serial.Serial(self.port, 9600, timeout=.1)
        self.targetSailAngle = 0
        self.targetRudderAngle = 0

    def setTargetSailAngle(self, targetSailAngle):
        self.targetSailAngle = targetSailAngle

    def setTargetRudderAngle(self, targetRudderAngle):
        self.targetRudderAngle = targetRudderAngle

    def sendData(self):
        sailString = str(self.targetSailAngle).zfill(3)
        rudderString = str(self.targetRudderAngle).zfill(3)
        dataString = sailString + rudderString + " "
        print(dataString)
        self.arduino.write(dataString.encode())