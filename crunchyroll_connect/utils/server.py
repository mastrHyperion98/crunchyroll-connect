from enum import Enum
import requests
import uuid

class RequestType(Enum):
    LOGIN = "login"
    LOGOUT = "logout"
    CREATE_SESSION = 'start_session'


class CrunchyrollServer:
    def __init__(self):
        self.domain = 'api.crunchyroll.com'
        self.token = 'LNDJgOit5yaRIWN'
        self.device_type = 'com.crunchyroll.windows.desktop'
        self.version = 0
        self.english = 'enUS'


    def getUrl(self, req):
       if not isinstance(req, RequestType):
           return "https://{}".format(self.domain)
       else:
           return "https://{}/{}.{}.json".format(self.domain, req.value, self.version)


    def start_session(self):
        url = self.getUrl(RequestType.CREATE_SESSION)
        params = {
            'access_token': self.token,
            'device_type': self.device_type,
            'device_id': uuid.uuid1(),
            'version': 1.1
        }
        response = requests.get(url, params)

        return response


    def login(self, account, password, session_id):
        url = self.getUrl(RequestType.LOGIN)
        data = {
            'account': account,
            'password': password,
            'session_id': session_id
        }

        response = requests.post(url, data)
        return response