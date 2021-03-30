from Data import *

class arduinoInputData:
    def __init__(self):
        self.target_sail_angle = 0
        self.target_gimbal_rudder_angle = angle()
        #arduino object with port, baud rate and timeout specified
        arduino = serial.Serial('COM4',9600,timeout=.1)

    def angle(self):
        data = arduino.readline()[:-1]
        #decode the data
        decoded_data = str(data,'utf-8')
        print(decoded_data)
        #grabs the first 3 symbols
        return decoded_data

    def getTargetSailAngle(self):
        return 0
    
    def getTargetRudderAngle(self):
        return angle()
