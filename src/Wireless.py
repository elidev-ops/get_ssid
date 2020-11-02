class Wireless:
    def __init__(self, data):
        self._wireless = self.createObject(data)

    def createObject(self, data):
        wireless = {}
        for i in data:
            wireless[i] = data[i]  
        return wireless