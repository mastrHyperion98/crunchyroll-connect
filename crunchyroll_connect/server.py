import requests

from .utils.collections import Series, Collection
from .utils.types import RequestType, Filters, Genres
from .utils.user import Config, User, datetime


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

        if self.__config.store['user'] is not None:
            current_datetime = datetime.now().astimezone().replace(microsecond=0)
            expires = self.__config.store['user'].expires

            if expires <= current_datetime:
                # If login session expired, login again
                self.logout()

            else:
                print('User is already logged in')
                return True

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
        print(response)
        # Note to check for expiration of the session and clear data to prevent re-using the same session maybe.
        if validate_request(response):
            # Create user object
            user_data = response['data']['user']
            user = User(
                user_id=user_data['user_id'],
                etp_guid=user_data['etp_guid'],
                username=user_data['username'],
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                premium=user_data['premium'],
                access_type=user_data['access_type'],
                created=user_data['created'],
                expires=response['data']['expires'],
                is_publisher=user_data['is_publisher']
            )

            self.__config.store['account'] = account
            self.__config.store['password'] = password
            self.__config.store['auth'] = response['data']['auth']
            self.__config.store['user'] = user

            return True

        return False

    def logout(self):

        if self.__config.store['user'] is None:
            raise ValueError('Illegal Operation: Cannot logout if User is not logged in!')

        url = self.get_url(RequestType.LOGOUT)
        data = {
            'user': self.__config.store['user_id'],
            'session_id': self.__config.store['session_id']
        }

        response = requests.post(url, data)

        if validate_request(response.json()):
            self.__config.clear_store()

            return True

        return False

    def end_session(self):
        self.__config.close_store()

    def fetch_locales(self):
        url = self.get_url(RequestType.LIST_LOCALES)

        data = {
            'session_id': self.__config.store['session_id'],
            'device_type': self.device_type,
            'device_id': self.__config.store['device_id']
        }
        response = requests.get(url, data).json()

        if validate_request(response):
            self.__config.store['cr_locales'] = response['data']
            return True

        return False

    def get_series_id(self, query):
        """
        Searches for the seriesID of an anime in the Crunchyroll catalogue. If it is present return the ID
        :param query: the name of the anime
        :return: the Crunchyroll series ID
        """
        url = self.get_url(RequestType.AUTOCOMPLETE)

        data = {
            'session_id': self.__config.store['session_id'],
            'device_type': self.device_type,
            'device_id': self.__config.store['device_id'],
            'q': query,
            'media_types': 'anime',
            'limit': 10  # Artificially limit to 10 results
        }

        response = requests.get(url, data).json()

        if validate_request(response):
            search_results = response['data']
            if len(search_results) < 1:
                return None

            for anime in response['data']:

                anime_name = anime['name'].lower()
                series_id = anime['series_id']
                search_query = query.lower()

                if anime_name == search_query:
                    return series_id

                else:
                    continue
        else:
            raise ValueError('Request Failed!\n\n{}'.format(response))

    def get_collection(self, series_id):

        url = self.get_url(RequestType.LIST_COLLECTION)

        data = {
            'session_id': self.__config.store['session_id'],
            'device_type': self.device_type,
            'device_id': self.__config.store['device_id'],
            'media_type': 'anime',
            'series_id': series_id
        }

        response = requests.get(url, data).json()

        if validate_request(response):
            data = response['data'][0]
            collection = Collection(
                availability_notes=data['availability_notes'],
                series_id=series_id,
                collection_id=data['collection_id'],
                etp_guid=data['etp_guid'],
                series_etp_guid=data['series_etp_guid'],
                complete=data['complete'],
                name=data['name'],
                description=data['description'],
                landscape_image=data['landscape_image'],
                portrait_image=data['portrait_image'],
                season=data['season'],
                created=data['created']
            )

            return collection
        else:
            raise ValueError('Request Failed!\n\n{}'.format(response))

    def list_series(self, limit: int = 10, offset: int = 0, filter_type: Filters = None, filter_tag: str = None):
        """
        Returns a list of series
        :param limit: The maximum number of items to return
        :param filter_tag: The tag, if any to be associated with the filter. Only if filter_type == PREFIX or TAG
        :param filter_type: The filter type as defined in utils.types.Filters
        :param offset: offset from the start to return. This enables a pagination system
        :return:
        """
        url = self.get_url(RequestType.LIST_SERIES)

        # If the passed in value is a genre get the string value
        if isinstance(filter_tag, Genres):
            filter_tag = filter_tag.value

        if filter_tag is not None and (filter_type == Filters.PREFIX or filter_type == Filters.TAG):
            tag = filter_type.value + filter_tag
        elif filter_type is not None:
            tag = filter_type.value
        else:
            tag = None

        data = {
            'session_id': self.__config.store['session_id'],
            'device_type': self.device_type,
            'device_id': self.__config.store['device_id'],
            'media_type': 'anime',
            'limit': limit,
            'offset': offset,
            'filter': tag
        }

        response = requests.get(url, data).json()
        if validate_request(response):
            series = []

            for el in response['data']:
                series.append(Series(
                    series_id=el['series_id'],
                    etp_guid=el['etp_guid'],
                    name=el['name'],
                    description=el['description'],
                    url=el['url'],
                    landscape_image=el['landscape_image'],
                    portrait_image=el['portrait_image'],
                ))

            return series

        else:
            raise ValueError('Request Failed!\n\n{}'.format(response))
