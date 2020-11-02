import re
import requests

class CreateError:
    def Status(self, data):
        try:
            value = self.Error(data.status_code)
            if not value:
                raise ValueError
            return value
        except ValueError:
            pass

        try:
            value =  self.Redirect(data.headers['Location'])
            if not value:
                raise ValueError
            return value
        except Exception:
            pass

        try:
            value =  self.Other(data.headers['Location'])
            if not value:
                raise ValueError
            return value
        except Exception:
            pass

        try:
            value = self.Success(data.headers['Location'])
            if not value:
                raise ValueError
            return value
        except Exception:
            pass


    def Error(self, data):
        if data in range(400, 500):
            return "Error"

    def Success(self, data):
        if 'index' in data.split('/')[3].split('.'):
            return "Success"

    def Redirect(self, data):
        if 'login' in data.split('/')[3].split('.'):
            return "Redirect"

    def Other(self, data):
        ip_urls = [
            '10.0.0.1',
            '10.0.1.1',
            '10.1.1.1',
            '192.168.0.1',
            '192.168.1.1',
            '192.168.2.1'
        ]
        if re.sub('[http://]', '', data) in ip_urls:
            return "Other"

test = CreateError()
s = requests.Session()
r = s.post('http://10.50.0.15:8080/LoguinCheck', data={'password':'MTIzNzg5'}, timeout=3.000, allow_redirects=False)
print(test.Status(r))