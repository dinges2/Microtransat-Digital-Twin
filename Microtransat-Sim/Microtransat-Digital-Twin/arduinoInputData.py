from inputDataInterface import *
import serial
import sys
class ArduinoInputData:
    def __init__(self):
        self.port = sys.argv[2]
        self.arduino = serial.Serial(self.port, 9600, timeout=.1)
        self.target_sail_angle = 0
        self.target_gimbal_rudder_angle = 0
        #arduino object with port, baud rate and timeout specified

    def rudderAngle(self):
        data = self.arduino.readline()[:-1]
        decoded_data = str(data,'utf-8')
        while decoded_data[0:6] != 'rudder':
            data = self.arduino.readline()[:-1]
            decoded_data = str(data,'utf-8')
        print(decoded_data)
        #grabs the first 3 symbols
        self.target_gimbal_rudder_angle = int(decoded_data[6:])
        return self.target_gimbal_rudder_angle

    def sailAngle(self):
        data = self.arduino.readline()[:-1]
        decoded_data = str(data,'utf-8')
        #decode the data
        while decoded_data[0:4] != 'sail':
            data = self.arduino.readline()[:-1]
            decoded_data = str(data,'utf-8')
        print(decoded_data)

        self.target_sail_angle = int(decoded_data[4:])
        return self.target_sail_angle

    def getTargetSailAngle(self):
        return self.sailAngle()

    def getTargetRudderAngle(self):
        return self.rudderAngle()