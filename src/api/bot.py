from instagrapi import Client
from instagrapi.types import Media, User, UserShort
import logging
import os

UserName = ""
PassWd = ""
Proxy = "http://127.0.0.1:10809"
Locale = "en_US"
IG_CREDENTIAL_PATH = ".\ig_settings.json"

settings = {
    'user_agent': 'Instagram 194.0.0.36.172 Android (26/8.0.0; 480dpi; 1080x1920; Xiaomi; MI 5s; capricorn; qcom; en_US; 301484483)',
    'country': 'US',
    'country_code': 1,
    'locale': 'en_US',
    'timezone_offset': -25200
}


    
class Bot:
    _cl = None
    def __init__(self):
        self._cl = Client(settings)
        
        self._cl.delay_range = [1, 3]
        self._cl.set_proxy(Proxy)
        self._cl.set_locale()
        self._cl.set_timezone_offset(-7 * 60 * 60)
        logging.info(f"Start logging...")
        if os.path.exists(IG_CREDENTIAL_PATH):
            self._cl.load_settings(IG_CREDENTIAL_PATH)
            self._cl.login(UserName, PassWd)
        else:
            self._cl.login(UserName, PassWd)
            self._cl.dump_settings(IG_CREDENTIAL_PATH)
        logging.debug(self._cl.get_timeline_feed())
    
    def getMedia(
        self,
        hashtags,
        ht_type="top",
        amount=27,
        ):
        ht_medias = []
        for hashtag in hashtags:
            # logging.info()
            if ht_type == "top":
                ht_medias.extend(
                    self._cl.hashtag_medias_top(name=hashtag, amount=amount if amount <= 9 else 9)
                )
            elif ht_type == "recent":
                ht_medias.extend(self._cl.hashtag_medias_recent(name=hashtag, amount=amount))
        return list(dict([(media.pk, media) for media in ht_medias]).values())
    def getUser(
        self,
        media : Media,
        ) -> User:
        # return self._cl.media_info_gql(int(media.pk)).dict()["user"]["pk"]
        logging.info("")
        return self._cl.user_info(media.user.pk)
    @staticmethod
    def getFollower_count(
        user: User
        ) -> int:
        return user.follower_count

class StarUser(User):
    pass