import requests
import uuid

from .types import RequestType
from .user import Config


def validate_request(req):

    if not isinstance(req, dict):
        return False

    if req['error'] == False and req['code'] == 'ok':
        return True
    else:
        return False


class CrunchyrollServer:
    def __init__(self):
        self.domain = 'api.crunchyroll.com'
        self.token = 'LNDJgOit5yaRIWN'
        self.device_type = 'com.crunchyroll.windows.desktop'
        self.version = 0
        self.english = 'enUS'
        self.is_logged_in = False
        self.__config = Config()
        self.__config.init_store()

    def get_url(self, req):
        if not isinstance(req, RequestType):
            return "https://{}".format(self.domain)
        else:
            return "https://{}/{}.{}.json".format(self.domain, req.value, self.version)

    def start_session(self):
        url = self.get_url(RequestType.CREATE_SESSION)

        device_id = self.__config.store['device_id']

        params = {
            'access_token': self.token,
            'device_type': self.device_type,
            'device_id': device_id,
            'version': 1.1
        }

        response = requests.get(url, params).json()
        if validate_request(response):
            self.__config.store['session_id'] = response['data']['session_id']
            self.__config.store['device_id'] = device_id

            return True

        return False

    def login(self, account=None, password=None):
        if account is None:
            account = self.__config.store['account']

        if password is None:
            password = self.__config.store['password']

        url = self.get_url(RequestType.LOGIN)
        data = {
            'account': account,
            'password': password,
            'session_id': self.__config.store['session_id']
        }

        response = requests.post(url, data).json()
        if validate_request(response):
            self.__config.store['account'] = account
            self.__config.store['password'] = password
            self.__config.store['auth'] = response['data']['auth']
            self.__config.store['user_id'] = response['data']['user']['user_id']

            self.is_logged_in = True
            return True

        return False

    def logout(self):
        url = self.get_url(RequestType.LOGOUT)
        data = {
            'user': self.__config.store['user_id'],
            'session_id': self.__config.store['session_id']
        }

        response = requests.post(url, data)

        if validate_request(response.json()):
            self.__config.clear_store()
            self.is_logged_in = False

            return True

        return False

    def end_session(self):
        self.__config.close_store()

