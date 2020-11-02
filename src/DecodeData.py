import base64

class DecodeData:
    def __init__(self, data):
        self._response = self.decode(data)
    

    def IsBase64(self, string):
        try:
            return base64.b64decode(string)
        except:
            return string

    def decode(self, data):
        res = data.split('\r')
        ssid = self.IsBase64(res[0]).decode('utf-8')
        security = self.IsBase64(res[13]).decode('utf-8')
        yield ssid, security, res[0], res[13]
