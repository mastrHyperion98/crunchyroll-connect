import requests
import uuid

from .types import RequestType


class CrunchyrollServer:
    def __init__(self):
        self.domain = 'api.crunchyroll.com'
        self.token = 'LNDJgOit5yaRIWN'
        self.device_type = 'com.crunchyroll.windows.desktop'
        self.version = 0
        self.english = 'enUS'

    def get_url(self, req):
        if not isinstance(req, RequestType):
            return "https://{}".format(self.domain)
        else:
            return "https://{}/{}.{}.json".format(self.domain, req.value, self.version)

    def start_session(self):
        url = self.get_url(RequestType.CREATE_SESSION)
        params = {
            'access_token': self.token,
            'device_type': self.device_type,
            'device_id': uuid.uuid1(),
            'version': 1.1
        }
        response = requests.get(url, params)

        return response

    def login(self, account, password, session_id):
        url = self.get_url(RequestType.LOGIN)
        data = {
            'account': account,
            'password': password,
            'session_id': session_id
        }

        response = requests.post(url, data)
        return response

    def logout(self, user, session_id):
        url = self.get_url(RequestType.LOGOUT)
        data = {
            'user': user,
            'session_id': session_id
        }

        response = requests.post(url, data)
        return response
