from datetime import datetime


class ImageSet:

    def __init__(self,
                 thumb_url: str,
                 small_url: str,
                 medium_url: str,
                 large_url: str,
                 full_url: str,
                 wide_url: str,
                 widestar_url: str,
                 fwide_url: str,
                 fwidestar_url: str,
                 width: str,
                 height: str):

        self.thumb_url = thumb_url
        self.small_url = small_url
        self.medium_url = medium_url
        self.large_url = large_url
        self.full_url = full_url
        self.wide_url = wide_url
        self.widestar_url = widestar_url
        self.fwide_url = fwide_url
        self.fwidestar_url = fwidestar_url
        self.width = width
        self.height = height


class Media:

    def __init__(self,
                 media_id: str,
                 etp_guid: str,
                 collection_id: str,
                 collection_etp_guid: str,
                 series_id: str,
                 series_etp_guid: str,
                 episode_number: str,
                 name: str,
                 description, str,
                 screenshot_image: ImageSet,
                 bif_uri: str,
                 uri: str,
                 clip: bool,
                 available: bool,
                 premium_available:bool,
                 free_available: bool,
                 availability_notes: str,
                 created: str,
                 playhead: int):

        self.class_type = 'media'
        self.media_id = media_id
        self.media_type = 'anime'
        self.etp_guid = etp_guid
        self.collection_id = collection_id
        self.collection_etp_guid = collection_etp_guid
        self.series_id = series_id
        self.series_etp_guid = series_etp_guid
        self.episode_number = episode_number
        self.name = name
        self.description = description
        self.screenshot_image = screenshot_image
        self.bif_uri = bif_uri
        self.uri = uri
        self.clip = clip
        self.available = available
        self.premium_available = premium_available
        self.free_available = free_available
        self.availability_notes = availability_notes
        self.created = datetime.strptime(created, "%Y-%m-%dT%H:%M:%S%z")
        self.playhead = playhead

    def __str__(self):
        return "\nclass_type: {}" \
                "\nmedia_id: {}" \
                "\nmedia_type: {}" \
                "\netp_guid: {}" \
                "\ncollection_id: {}" \
                "\ncollection_etp_guid: {}" \
                "\nseries_id: {}" \
                "\nseries_etp_guid: {}" \
                "\nepisode_number: {}" \
                "\nname: {}" \
                "\ndescription: {}" \
                "\nscreenshot_image: {}" \
                "\nbif_uri: {}" \
                "\nuri: {}" \
                "\nclip: {}" \
                "\navailable: {}" \
                "\npremium_available: {}" \
                "\nfree_available: {}" \
                "\navailability_notes: {}" \
                "\ncreated: {}" \
                "\nplayhead: {}".format(self.class_type,
                                        self.media_id,
                                        self.media_type,
                                        self.etp_guid,
                                        self.collection_id,
                                        self.collection_etp_guid,
                                        self.series_id,
                                        self.series_etp_guid,
                                        self.episode_number,
                                        self.name,
                                        self.description,
                                        self.screenshot_image,
                                        self.bif_uri,
                                        self.uri,
                                        self.clip,
                                        self.available,
                                        self.premium_available,
                                        self.free_available,
                                        self.availability_notes,
                                        self.created,
                                        self.playhead)



