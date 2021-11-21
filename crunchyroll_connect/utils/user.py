import shelve
import os
import uuid


class Config:

    def __init__(self):
        self.store = None

    def init_store(self):
        if os.path.isfile('user'):
            # File exists
            self.store = shelve.open('user')

        else:
            store = shelve.open('user')
            store['session_id'] = ""
            store['device_id'] = uuid.uuid1()
            store['account'] = ""
            store['password'] = ""
            store['auth'] = ""
            store['user_id'] = ""
            store['cr_locales'] = None

            self.store = store

    def clear_store(self):
        if self.store is None:
            self.init_store()

        self.store['session_id'] = ""
        self.store['account'] = ""
        self.store['password'] = ""
        self.store['auth'] = ""
        self.store['user_id'] = ""
        self.store['cr_locales'] = None
        self.store.sync()

    def close_store(self):
        self.store.sync()
        self.store.close()
