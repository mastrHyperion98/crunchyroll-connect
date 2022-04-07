import shelve
import os
import uuid
from datetime import datetime


class User:
    # Note the use of var : type is only for debugging and readability. Python is not statically typed so data type can
    # be changed on a whim through assignment
    def __init__(self,
                 user_id: int,
                 etp_guid: str,
                 username: str,
                 email: str,
                 first_name: str,
                 last_name: str,
                 premium: str,
                 access_type: str,
                 created: str,
                 expires: str,
                 is_publisher: bool = False):

        self._class = 'user'
        self.user_id = user_id
        self.etp_guid = etp_guid
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.premium = premium
        self.access_type = access_type
        self.created = datetime.strptime(created, "%Y-%m-%dT%H:%M:%S%z")
        self.expires = datetime.strptime(expires, "%Y-%m-%dT%H:%M:%S%z")
        self.is_publisher = is_publisher


class Config:

    def __init__(self):
        self.store = None

    def init_store(self):
        if os.path.isfile('user.dat'):
            # File exists
            self.store = shelve.open('user.dat')

        else:
            store = shelve.open('user.dat')
            store['session_id'] = ""
            store['device_id'] = uuid.uuid1()
            store['account'] = ""
            store['password'] = ""
            store['user'] = None
            store['auth'] = ""
            store['user_id'] = ""
            store['cr_locales'] = None

            self.store = store

    def clear_store(self):
        if self.store is None:
            self.init_store()

        #self.store['session_id'] = ""
        self.store['account'] = ""
        self.store['password'] = ""
        self.store['user'] = None
        self.store['auth'] = ""
        self.store['user_id'] = ""
        self.store['cr_locales'] = None
        self.store.sync()

    def is_logged_in(self):
        return self.store['account'] != "" and self.store['password'] != ""

    def close_store(self):
        self.store.sync()
        self.store.close()
