from datetime import datetime

from crunchyroll_connect.utils.user import User


class Session:
    def __init__(self, session_id, device_id):
        self.session_id = session_id
        self.user = None
        self.auth = None
        self.locales = None
        self.device_id = device_id

    def create_session(self, user: User, auth, locales, device_id, session_id):
        self.user = user
        self.auth = auth
        self.locales = locales
        self.device_id = device_id
        self.session_id = session_id

    def has_user(self):
        return self.user is not None

    def get_user(self):
        return self.user

    def toJSON(self):
        return {
            "session_id": self.session_id,
            "user": self.user.toJSON(),
            "auth": self.auth,
            "locales": self.locales,
            "device_id": self.device_id
        }
