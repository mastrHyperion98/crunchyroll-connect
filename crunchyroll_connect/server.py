from datetime import timedelta

import re
import requests
import m3u8
import uuid

from .utils.Session import Session
from .utils.collections import Series, Collection
from .utils.types import RequestType, Filters, Genres
from .utils.user import User, datetime
from .utils.media import Media, MediaStream


def get_id():
    # ID will be tied to the mac_address of the NIC
    current_machine_id = (':'.join(re.findall('..', '%012x' % uuid.getnode())))
    return current_machine_id


def validate_request(req):
    if not isinstance(req, dict):
        return False

    if req['error'] is False and req['code'] == 'ok':
        return True
    else:
        return False


def login_needed(session):
    is_valid = True

    if session.has_user():
        user = session.user
        if user.is_expired():
            return is_valid

        is_valid = False

    return is_valid


def login_required(function):
    def wrap(self, *args, **kwargs):
        if self.server_session.has_user() and len(self.server_session.auth) > 0:
            return function(self, *args, **kwargs)
        else:
            raise ValueError('Must be logged in to access to function')

    return wrap


# Evaluate if session is valid
def session_required(function):
    def wrap(self, *args, **kwargs):
        if self.server_session.session_id is not None:
            return function(self, *args, **kwargs)
        else:
            raise ValueError('Illegal action: A valid session must be started.')

    return wrap


def res_to_quality(resolution):
    if resolution == '1280x720':
        return "high"
    if resolution == '1920x1080':
        return "ultra"
    if resolution == '848x480':
        return "mid"
    if resolution == '640x360':
        return "low"
    else:
        return "lowest"


class CrunchyrollServer:
    def __init__(self):
        self.domain = 'api.crunchyroll.com'
        self.token = 'LNDJgOit5yaRIWN'
        self.device_type = 'com.crunchyroll.windows.desktop'
        self.device_id = get_id()
        self.version = 0
        self.english = 'enUS'
        self.session = requests.Session()
        self.server_session: Session = None

    def get_url(self, req):
        if not isinstance(req, RequestType):
            return "https://{}".format(self.domain)
        else:
            return "https://{}/{}.{}.json".format(self.domain, req.value, self.version)

    def mock_call(self):
        """
        Given a session attempt a mock connection to validate the session
        :param request: Request session object
        :param session: A valid Crunchyroll session object
        :return:
        """

        if not isinstance(self.session, Session):
            raise Exception(f"{self.session} is not instance of Session")

        url = self.get_url(RequestType.INFO)

        data = {
            'session_id': self.server_session.session_id,
            'device_type': self.device_type,
            'device_id': self.server_session.device_id,
            'media_type': 'anime',
            'media_id': 796204,
            'fields': 'media.stream_data,media.playhead'
        }

        response = self.session.get(url, params=data, cookies=self.session.cookies).json()
        if not validate_request(response):
            raise Exception(f"{response['error']} {response['message']}")

    def start(self, email, password, session=None):
        if session is not None:
            try:
                self.mock_call()
            except:
                self.server_session = self.__create_session()
        else:
            self.server_session = self.__create_session()

        # Always end with a login attempt
        self.__login(email, password)

    def __create_session(self):
        """
        Creates and stores a new Crunchyroll Session
        """

        url = self.get_url(RequestType.CREATE_SESSION)

        params = {
            'access_token': self.token,
            'device_type': self.device_type,
            'device_id': self.device_id,
            'version': 1.1
        }

        response = self.session.post(url, params, cookies=self.session.cookies).json()
        if validate_request(response):
            crunchyroll_session = Session(response['data']['session_id'], self.device_id)
            return crunchyroll_session

        else:
            raise ValueError('Request Failed!\n\n{}'.format(response))

    def __login(self, account, password):
        if not isinstance(account, str):
            raise Exception(f"{account} is not of type str")

        if not isinstance(password, str):
            raise Exception(f"{password} is not of type str ")

        # Check if login is required or if the session and login are still valide
        if not login_needed(self.server_session):
            return True

        url = self.get_url(RequestType.LOGIN)
        data = {
            'account': account,
            'password': password,
            'session_id': self.server_session.session_id
        }

        response = self.session.post(url, data).json()
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
                expires=datetime.now() + timedelta(hours=12),
                is_publisher=user_data['is_publisher']
            )

            self.server_session.auth = response['data']['auth']
            self.server_session.user = user

            return True

        else:
            raise ValueError(F"Login Failed - {response['error']} {response['message']} ")

    @login_required
    @session_required
    def logout(self):
        url = self.get_url(RequestType.LOGOUT)
        params = {
            'access_token': self.token,
            'device_type': self.device_type,
            'device_id': self.server_session.device_id,
            'version': 1.1,
            'auth': self.server_session.auth
        }

        response = self.session.post(url, params, cookies=self.session.cookies).json()
        if validate_request(response):
            self.session.cookies.clear()
            print("logged out")
        else:
            raise ValueError('Request Failed!\n\n{}'.format(response))

    def close(self):
        self.session.close()

    @session_required
    def fetch_locales(self):
        url = self.get_url(RequestType.LIST_LOCALES)

        data = {
            'session_id': self.server_session.session_id,
            'device_type': self.device_type,
            'device_id': self.server_session.device_id
        }
        response = self.session.get(url, data).json()

        if validate_request(response):
            self.server_session.locales = response['data']
            return True

        else:
            raise ValueError('Request Failed!\n\n{}'.format(response))

    @session_required
    def get_series_id(self, query):
        """
        Searches for the seriesID of an anime in the Crunchyroll catalogue. If it is present return the ID
        :param query: the name of the anime
        :return: the Crunchyroll series ID
        """
        url = self.get_url(RequestType.AUTOCOMPLETE)

        data = {
            'session_id': self.server_session.session_id,
            'device_type': self.device_type,
            'device_id': self.server_session.device_id,
            'q': query,
            'media_types': 'anime',
            'limit': 10  # Artificially limit to 10 results
        }

        response = self.session.get(url, params=data, cookies=self.session.cookies).json()
        if validate_request(response):
            search_results = response['data']
            if len(search_results) < 1:
                return -1  # Some random value

            for anime in response['data']:

                anime_name = anime['name'].lower()
                series_id = anime['series_id']
                search_query = query.lower()

                if search_query in anime_name:
                    return series_id

                else:
                    continue
        else:
            raise ValueError('Request Failed!\n\n{}'.format(response))

    @session_required
    def get_collections(self, series_id):

        url = self.get_url(RequestType.LIST_COLLECTION)

        data = {
            'session_id': self.server_session.session_id,
            'device_type': self.device_type,
            'device_id': self.server_session.device_id,
            'media_type': 'anime',
            'series_id': series_id
        }

        response = self.session.get(url, params=data, cookies=self.session.cookies).json()

        if validate_request(response):
            data = response['data']

            collections = []
            for el in data:
                collection = Collection(
                    availability_notes=el['availability_notes'],
                    series_id=series_id,
                    collection_id=el['collection_id'],
                    etp_guid=el['etp_guid'],
                    series_etp_guid=el['series_etp_guid'],
                    complete=el['complete'],
                    name=el['name'],
                    description=el['description'],
                    landscape_image=el['landscape_image'],
                    portrait_image=el['portrait_image'],
                    season=el['season'],
                    created=el['created']
                )

                # if "dub" not in collection.name.lower():
                collections.append(collection)

            return collections
        else:
            raise ValueError('Request Failed!\n\n{}'.format(response))

    @session_required
    def filter_series(self, limit: int = 10, offset: int = 0, filter_type: Filters = None, filter_tag: str = None):
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
            'session_id': self.server_session.session_id,
            'device_type': self.device_type,
            'device_id': self.server_session.device_id,
            'media_type': 'anime',
            'limit': limit,
            'offset': offset,
            'filter': tag
        }

        response = self.session.get(url, params=data, cookies=self.session.cookies).json()

        try:
            series = self.extract_series(response)
            return series
        except:
            return []

    @session_required
    def get_episodes(self, collection_id, limit=1000, offset=0):
        url = self.get_url(RequestType.LIST_MEDIA)

        data = {
            'session_id': self.server_session.session_id,
            'device_type': self.device_type,
            'device_id': self.server_session.device_id,
            'media_type': 'anime',
            'limit': limit,
            'offset': offset,
            'collection_id': collection_id
        }

        response = self.session.get(url, params=data, cookies=self.session.cookies).json()

        if validate_request(response):
            media_list = []
            episode_list = response['data']

            for ep in episode_list:
                media_list.append(Media(
                    media_id=ep['media_id'],
                    etp_guid=ep['etp_guid'],
                    collection_id=ep['collection_id'],
                    collection_etp_guid=ep['collection_etp_guid'],
                    series_id=ep['series_id'],
                    series_etp_guid=ep['series_etp_guid'],
                    episode_number=ep['episode_number'],
                    name=ep['name'],
                    description=ep['description'],
                    screenshot_image=ep['screenshot_image'],
                    bif_url=ep['bif_url'],
                    url=ep['url'],
                    clip=ep['clip'],
                    available=ep['available'],
                    premium_available=ep['premium_available'],
                    free_available=ep['free_available'],
                    availability_notes=ep['availability_notes'],
                    created=ep['created'],
                    playhead=ep['playhead']))

            return media_list

        else:
            raise ValueError('Request Failed!\n\n{}'.format(response))

    @login_required
    @session_required
    def get_media_stream(self, media_id):
        url = self.get_url(RequestType.INFO)

        data = {
            'session_id': self.server_session.session_id,
            'device_type': self.device_type,
            'device_id': self.server_session.device_id,
            'media_type': 'anime',
            'media_id': media_id,
            'fields': 'media.stream_data,media.playhead'
        }

        response = self.session.get(url, params=data, cookies=self.session.cookies).json()
        if validate_request(response):
            stream_data = response['data']['stream_data']['streams']
            expires = stream_data[0]['expires']
            url = stream_data[0]["url"]

            playlist = m3u8.load(url)  # this could also be an absolute filename
            m3u8_playlist = playlist.data['playlists']
            media_streams = {}
            visited_resolutions = []
            urls = []
            for i in range(len(m3u8_playlist)):
                # Don't visit duplicates

                stream = m3u8_playlist[i]
                resolution = stream['stream_info']['resolution']
                if (resolution not in visited_resolutions):
                    quality = res_to_quality(resolution)
                    url = stream['uri']
                    media_stream = MediaStream(quality, expires, url)
                    media_streams[quality] = media_stream
                    visited_resolutions.append(resolution)

            return media_streams

        else:
            raise ValueError('Request Failed!\n\n{}'.format(response))

    @session_required
    def search(self, q, media_type, filter=None, limit=10, offset=0):
        url = self.get_url(RequestType.AUTOCOMPLETE)

        data = {
            'session_id': self.server_session.session_id,
            'device_type': self.device_type,
            'device_id': self.server_session.device_id,
            'media_types': media_type,
            'q': q,
            'limit': limit,
            'offset': offset,
            'filter': filter
        }

        response = self.session.get(url, params=data, cookies=self.session.cookies).json()

        try:
            series = self.extract_series(response)
            return series
        except:
            return []

    def extract_series(self, response):
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
