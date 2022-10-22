from kavenegar import *

from config import settings

class KavenegarSMS:

    def __init__(self):
        self.api = KavenegarAPI(settings.KAVENEGAR_API_KEY)

    def register(self, receptor=None, code=None, password=None):
        self.params = {
            'receptor': receptor,
            'template': 'register',
            'token': code,
            'type': 'sms'
        }

    def otp(self, receptor=None,code=None):
        self.params = {
        'receptor': receptor,
        'template': 'irancafeotp',
        'token': code,
        'type': 'sms'
        }

    def send(self):
        flag = True
        for i, j in self.params.items():
            if j is None:
                flag = False
        if flag:
            try:
                return self.api.verify_lookup(self.params)
            except APIException as e:
                return e
            except HTTPException as e:
                return e
        else:
            raise APIException