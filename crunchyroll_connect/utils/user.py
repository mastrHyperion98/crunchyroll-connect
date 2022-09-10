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
                 expires: datetime,
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
        self.expires = expires
        self.is_publisher = is_publisher

    def is_expired(self):
        current_datetime = datetime.now()
        if current_datetime <= self.expires:
            return True
        else:
            return False

    def toJSON(self):

        return {
            "class": self._class,
            "user_id": self.user_id,
            "etp_guid": self.etp_guid,
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "premium": self.premium,
            "access_type": self.access_type,
            "created": self.created,
            "expires": self.expires,
            "is_publisher": self.is_publisher
        }
