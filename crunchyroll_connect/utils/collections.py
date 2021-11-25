from media import ImageSet


class Series:

    def __init__(self,
                 series_id: str,
                 etp_guid: str,
                 name: str,
                 description: str,
                 url: str,
                 media_count: int,
                 landscape_image: ImageSet,
                 portrait_image: ImageSet
                 ):
        self.media_type = "anime",
        self.series_id = series_id,
        self.etp_guid = etp_guid,
        self.name = name,
        self.description = description,
        self.url = url,
        self.media_count = media_count,
        self.landscape_image = landscape_image,
        self.portrait_image = portrait_image


class Collection:

    def __init__(self,
                 availability_notes: str,
                 series_id: str,
                 collection_id: str,
                 complete: bool,
                 name: str,
                 description: str,
                 landscape_image: ImageSet,
                 portrait_image: ImageSet,
                 season: str,
                 created: str):

        self.availability = availability_notes,
        self.media_type = 'anime',
        self.series_id = series_id,
        self.collection_id = collection_id,
        self.completed = complete,
        self.name = name,
        self.description = description,
        self.landscape_image = landscape_image,
        self.portrait_image = portrait_image,
        self.season = season,
        self.created = created
