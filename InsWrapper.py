from ins import Ins
from db.database import DatabaseManager
import config


# you must have your login cookie
COOKIE = config.cookie
DATA_PATH = "./data.csv"
CTRL_PATH = "./gui_to_spider.json"


class InsWrapper(Ins):
    def __init__(self):
        super().__init__(COOKIE)
        self.db = DatabaseManager()

    def get_UserData(self, keywords: list, mode: str, amount: int):
        for keyword in keywords:
            counter = 0
            username_lst = self.getUsernameBytag(keyword, mode=mode)
            counter = 0
            for username in username_lst:
                if counter >= amount:
                    break
                
                insert_sql = "insert into users (biography,username,fbid,full_name,id,followed_by,follow,noteCount,is_private,is_verified) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                userInfo = self.get_userInfo(username)
                userInfo.pop("avatar", "N/A")
                # print(userInfo)
                values = list(userInfo.values())
                self.db.execute_insert(insert_sql, values)
                counter += 1
                self.randSleep([60,95])

    def get_postsByUsername(self, username: str, amount: int):
        """Args:
            username (str): username
            amount (int): user recent posts number
            Return: post list
        """
        post_lst = []
        counter = 0
        posts = self.get_userPosts(username)
        insert_sql = "insert into posts (code, id, pk_id, comment_count, like_count, txt, create_at) values (%s, %s, %s, %s, %s, %s, %s)"
        for post in posts:
            if counter >= amount:
                break
            post.pop("photo", "N/A")
            post.pop("video", "N/A")
            # print(post)
            values = list(post.values())
            self.db.execute_insert(insert_sql, values)
            post_lst.append(post)
            counter+=1
            self.randSleep([60,95])
        return post_lst


INS = InsWrapper()
# INS.get_postsByUsername("nasa", 5)
INS.get_UserData(["minecraft"], "top", 3)