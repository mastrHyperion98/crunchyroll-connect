from enum import Enum


class RequestType(Enum):
    LOGIN = 'login'
    LOGOUT = 'logout'
    CREATE_SESSION = 'start_session'
    LIST_LOCALES = 'list_locales'
    LIST_MEDIA = 'list_media'
    LIST_COLLECTION = 'list_collections'
    INFO = 'info'
    CATEGORIES = 'categories'
