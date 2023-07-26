from instagrapi import Client
from instagrapi.types import Media, User
import logging
from instagrapi.exceptions import LoginRequired, PleaseWaitFewMinutes, ClientError

from time import sleep
from functools import wraps
UserName = "sonmudef"
PassWd = "Son5Mu159"
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

def retry(times, expections):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            while times > 0:
                try:
                    return func(*args, **kwargs)
                except expections as e:
                    times -= 1
                    if times == 0:
                        raise e
                sleep(10)
                
        return wrapper
    return decorator
    
class Bot:
    _cl = None
    def __init__(self):
        self._cl = Client(settings)
        
        self._cl.delay_range = [3,5]
        self._cl.set_proxy(Proxy)
        self._cl.set_locale()
        self._cl.set_timezone_offset(-7 * 60 * 60)
        login_via_session = False
        login_via_pw = False
        try:
            session = self._cl.load_settings(IG_CREDENTIAL_PATH)
            login_via_session = True
        except :
            pass
        if login_via_session == True and session:
            try:
                self._cl.set_settings(session)
                self._cl.login(UserName, PassWd)

                # check if session is valid
                try:
                    self._cl.get_timeline_feed()
                except LoginRequired:
                    logging.warning("Session is invalid, need to login via username and password")

                    old_session = self._cl.get_settings()

                    # use the same device uuids across logins
                    self._cl.set_settings({})
                    self._cl.set_uuids(old_session["uuids"])

                    self._cl.login(UserName, PassWd)
                login_via_session = True
            except Exception as e:
                logging.warning("Couldn't login user using session information: %s" % e)

        if not login_via_session:
            try:
                logging.warning("Attempting to login via username and password. username: %s" % UserName)
                if self._cl.login(UserName, PassWd):
                    login_via_pw = True
                    self._cl.dump_settings(IG_CREDENTIAL_PATH)
            except Exception as e:
                logging.warning("Couldn't login user using username and password: %s" % e)

        if not login_via_pw and not login_via_session:
            raise Exception("Couldn't login user with either password or session")
                        
    def getMedia(
        self,
        hashtags,
        ht_type="top",
        amount=27,
        ):
        ht_medias = []
        for hashtag in hashtags:
            try:
                # logging.info()
                if ht_type == "top":
                    ht_medias.extend(
                        self._cl.hashtag_medias_top(name=hashtag, amount=amount if amount <= 9 else 9)
                    )
                elif ht_type == "recent":
                    ht_medias.extend(self._cl.hashtag_medias_recent(name=hashtag, amount=amount))
            except PleaseWaitFewMinutes:
                logging.warning("Detected")
                sleep(15)
                try:
                    self._cl.set_settings(session)
                    self._cl.login(UserName, PassWd)

                    # check if session is valid
                    try:
                        self._cl.get_timeline_feed()
                    except LoginRequired:
                        logging.warning("Session is invalid, need to login via username and password")

                        old_session = self._cl.get_settings()

                        # use the same device uuids across logins
                        self._cl.set_settings({})
                        self._cl.set_uuids(old_session["uuids"])

                        self._cl.login(UserName, PassWd)
                    login_via_session = True
                except Exception as e:
                    logging.warning("Couldn't login user using session information: %s" % e)

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