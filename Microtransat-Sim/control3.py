from simpylc import *
# from data import *

class Control(Module):
    def __init__(self):
        Module.__init__(self)
        # self.data = Data()
        self.page('sailboat movement control')

        self.group('control', True)
        self.movement_speed = Register(0)

        self.group('sail')
        self.target_sail_angle = Register()

        self.group('rudder')
        self.target_gimbal_rudder_angle = Register()

    def sweep(self):
        if self.target_sail_angle > 90:
            self.target_sail_angle.set(90)
        # self.target_sail_angle.set(self.data.sail_angle)
        if self.target_sail_angle < -90:
            self.target_sail_angle.set(-90)

        if self.target_gimbal_rudder_angle > 45:
            self.target_gimbal_rudder_angle.set(45)
        
        if self.target_gimbal_rudder_angle < -45:
            self.target_gimbal_rudder_angle.set(-45)