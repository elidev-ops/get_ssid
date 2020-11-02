import requests
import re

from CreateStatus import CreateStatus

class Connection:
    def __init__(self, password = 'admin'):
        self.payload = {
            'checkEn': 0,
            'Username': 'admin',
            'Password': password
        }

        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
        }
    
    def DefaultConnect(self, data):
        url_payload = 'http://%s:%s'%(data['ip'], data['port'])
        try:
            self.session.post('%s/LoginCheck '%url_payload, data=self.payload, headers=self.headers, timeout=3.000, allow_redirects=False)
            response = self.session.get('%s/goform/wirelessGetSecurity'%url_payload, timeout=3.000)
            return response
        except Exception:
            pass

    def RouterPasswordOnly(self, data):
        url_raw = 'http://%s:%s'%(data['ip'], data['port'])
        try:
            request = self.session.post('%s/login/Auth'%url_raw, data={'password':'MTIzNzg5'}, timeout=3.000, allow_redirects=False)
            if 'Set-Cookie' not in request.headers:
                self.session.post('%s/login/Auth'%url_raw, data={'password':'YWRtaW4='}, timeout=3.000, allow_redirects=False)
            response = self.session.get('%s/goform/getWifi?modules=wifiBasicCfg'%url_raw, timeout=3.000)
            return response
        except Exception:
            return

    def WrongPasswordTry(self, data):
        self.payload['Password'] = 'admin'
        response = self.DefaultConnect(data)
        return response
    
    def ErrConnectionHost(self):
        return

    def ConnectionStatusRetry(self, data):
        return {
            'Error': self.ErrConnectionHost(),
            'Redirect': self.WrongPasswordTry(data),
            'Success': self.DefaultConnect(data),
            'Other': self.RouterPasswordOnly(data)
        }

    def connect(self, url, port = 8080):
        url_init = 'http://%s:%s/LoginCheck'%(url, port)
        url_obj = {
            'ip': url,
            'port': port
        }

        try:
            request = self.session.post(url_init, data=self.payload, headers=self.headers, timeout=3.000, allow_redirects=False)
            status = CreateStatus()
            get_status = status.GetStatus(request)
            response = self.ConnectionStatusRetry(url_obj)[get_status]          
            return response
        except Exception:
            pass