from enum import Enum

class RequestType(Enum):
    LOGIN = "login"
    LOGOUT = "logout"
    CREATE_SESSION = 'start_session'