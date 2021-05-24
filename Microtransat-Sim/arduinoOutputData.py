from outputDataInterface import *
from arduinoInputData import *
import serial
import sys

class ArduinoOutputData:

    def __init__(self):
        self.port = 'COM5'
        self.arduino = serial.Serial(self.port, 9600, timeout=.1)


    def setTargetSailAngle(self, data):
        # data = self.sailAngle()
        self.arduino.write(data)

    def setTargetRudderAngle(self, data):
        # data = self.rudderAngle()
        self.arduino.write(data)


# import serial
# import time
#
# arduino = serial.Serial('COM5', 9600)
#
#
# def stuur_character_HIGH():
#     arduino.write(l.encode())
#     print("sending", l)
#     time.sleep(1)
#
#
# def stuur_character_LOW():
#     # encode string to arduino
#     arduino.write(l.encode())
#     print("sending", l)
#     time.sleep(1)
#
#
# stuur_character_HIGH()
# time.sleep(2)
# stuur_character_HIGH()
# while (True):
#     if (arduino.in_waiting > 0):
#         data = arduino.readline()[:-2]
#         decoded_data = str(data, 'utf-8')
#         print("arduino:", decoded_data)
