import requests

class ESP_data:
    def __init__(self):
        pass

    def getTargetSailAngle(self):
        URL = "http://192.168.1.1/getTargetSailAngle"
        r = requests.get(url = URL)
        print(r.text)
        return int(r.text)

    def getTargetRudderAngle(self):
        URL = "http://192.168.1.1/getTargetRudderAngle"
        r = requests.get(url = URL)
        return int(r.text)

    def setTargetSailAngle(self, angle):
        URL = "http://192.168.1.1/setTargetSailAngle"
        PARAMS = {'targetSailAngle': str(angle) }
        r = requests.get(url = URL, params = PARAMS)

    def setTargetRudderAngle(self, angle):
        URL = "http://192.168.1.1/setTargetRudderAngle"
        PARAMS = {'targetRudderAngle':str(angle)}
        r = requests.get(url = URL, params = PARAMS)
        print(r)