import time

class OutputDataInterface:
    def __init__(self):
        self.targetSailAngle = 0
        self.targetRudderAngle = 0

    def setTargetSailAngle(self):
        return self.targetSailAngle

    def setTargetRudderAngle(self):
        return self.targetRudderAngle