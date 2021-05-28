from simpylc import *

from arduinoInputData import *
from arduinoOutputData import *


class Control(Module):
    def __init__(self):
        Module.__init__(self)
        # if len(sys.argv) > 1 and sys.argv[1] == 'arduino':
        self.data = ArduinoInputData()
        self.send = ArduinoOutputData()
        self.page('sailboat movement control')

        self.group('control', True)
        self.movement_speed = Register(0)

        self.group('sail')
        self.target_sail_angle = Register()

        self.group('rudder')
        self.target_gimbal_rudder_angle = Register()

        self.group('pause')
        self.pause = Marker()

    def sweep(self):
        if len(sys.argv) > 1:
            self.target_sail_angle = Register(self.data.getTargetSailAngle())
            self.target_gimbal_rudder_angle = Register(self.data.getTargetRudderAngle())
            self.send.setTargetSailAngle(self.target_sail_angle._state)
            self.send.setTargetRudderAngle(self.target_gimbal_rudder_angle._state)
            self.send.sendData()


        # if self.target_sail_angle > 90:
        #     self.target_sail_angle.set(90)
        
        # if self.target_sail_angle < -90:
        #     self.target_sail_angle.set(-90)
        
        # if self.target_gimbal_rudder_angle > 45:
        #     self.target_gimbal_rudder_angle.set(45)
        
        # if self.target_gimbal_rudder_angle < -45:
        #     self.target_gimbal_rudder_angle.set(-45)