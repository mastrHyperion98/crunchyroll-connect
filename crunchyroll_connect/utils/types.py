from enum import Enum


class RequestType(Enum):
    LOGIN = 'login'
    LOGOUT = 'logout'
    CREATE_SESSION = 'start_session'
    LIST_LOCALES = 'list_locales'
    LIST_MEDIA = 'list_media'
    LIST_COLLECTION = 'list_collections'
    LIST_SERIES = 'list_series'
    INFO = 'info'
    CATEGORIES = 'categories'
    AUTOCOMPLETE = 'autocomplete'
    SEARCH = 'search'


class Filters(Enum):
    ALPHA = 'alpha'
    FEATURED = 'featured'
    NEWEST = 'newest'
    POPULAR = 'popular'
    PREFIX = 'prefix:'
    SIMULCAST = 'simulcast'
    TAG = 'tag:'
    UPDATED = 'updated'


class Genres(Enum):
    ACTION = 'action'
    ADVENTURE = 'adventure'
    COMEDY = 'comedy'
    DRAMA = 'drama'
    FANTASY = 'fantasy'
    HAREM = 'harem'
    HISTORICAL = 'historical'
    IDOLS = 'idols'
    ISEKAI = 'isekai'
    MAGICAL_GIRLS = 'magical girls'
    MECHA = 'mecha'
    MUSIC = 'music'
    MYSTERY = 'mystery'
    POST_APOCALYPTIC = 'post-apocalyptic'
    ROMANCE = 'romance'
    SCIFI = 'sci-fi'
    SEINEN = 'seinen'
    SHOJO = 'shojo'
    SHONEN = 'shonen'
    SLICE_OF_LIFE = 'slice of life'
    SPORTS = 'sports'
    SUPERNATURAL = 'supernatural'
    THRILLER = 'thriller'