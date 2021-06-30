from simpylc import *
import sys
from inputDataInterface import *
from arduinoInputData import *
from ArduinoOutputData import *
from client import *
class Control(Module):
    def __init__(self):
        Module.__init__(self)
        # self.ESPdata = ESP_data()
        # self.arduinoInputData = ArduinoInputData()
        # self.arduinoOutputData = ArduinoOutputData()
        self.page('sailboat movement control')

        self.group('control', True)
        self.movement_speed = Register(0)

        self.group('sail')
        self.target_sail_angle = Register()

        self.group('rudder')
        self.target_gimbal_rudder_angle = Register()

        self.group('pause')
        self.pause = Marker()

        self.group('rotate sail')
        self.rotateSail = Marker()

    def sweep(self):
        pass
        # Arduino input:
        # self.target_sail_angle = Register(self.arduinoInputData.getTargetSailAngle())
        # self.target_gimbal_rudder_angle = Register(self.arduinoInputData.getTargetRudderAngle())

        # Aruino output:
        # self.arduinoOutputData.setTargetSailAngle(self.target_sail_angle._state)
        # self.arduinoOutputData.setTargetRudderAngle(self.target_gimbal_rudder_angle._state)

        # ESP input:
        # self.target_sail_angle = Register(self.ESPdata.getTargetSailAngle())
        # self.target_gimbal_rudder_angle = Register(self.ESPdata.getTargetRudderAngle())

        # ESP output:
        # self.ESPdata.setTargetSailAngle(self.target_sail_angle._state)
        # self.ESPdata.setTargetRudderAngle(self.target_gimbal_rudder_angle._state) 