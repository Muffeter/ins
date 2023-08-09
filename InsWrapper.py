from ins import Ins
from db.database import DatabaseManager
import config
import datetime


# you must have your login cookie
COOKIE = config.cookie

class InsWrapper(Ins):
    def __init__(self):
        super().__init__(COOKIE)
        self.db = DatabaseManager()

    def get_UserData(self, keywords: list, mode: str, amount: int):
        for keyword in keywords:
            counter = 0
            username_lst = self.getUsernameBytag(keyword, mode=mode)
            for username in username_lst:
                if counter >= amount:
                    break
                insert_sql = "insert into users (biography,username,fbid,full_name,user_id,followed_by,follow,noteCount,is_private,is_verified,business_email) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                userInfo = self.get_userInfo(username)
                userInfo.pop("avatar", "N/A")
                values = list(userInfo.values())
                self.db.execute_insert(insert_sql, values)
                counter += 1
                self.randSleep([60,95])
            self.db.remove_duplicate_rows()

    def get_postsByUsername(self, username: str, amount: int):
        """Args:
            username (str): username
            amount (int): user recent posts number
            Return: post list
        """
        
        post_lst = []
        counter = 0
        posts = self.get_userPosts(username)
        insert_sql = "insert into posts (code,user_id,comment_count,like_count,introduction,create_time) values (%s, %s, %s, %s, %s, %s)"
        for post in posts:
            if counter >= amount:
                break
            post['create_time'] = datetime.datetime.fromtimestamp(int(post['create_time'])).strftime("%Y-%m-%d %H:%M:%S")
            
            values = list(post.values())
            self.db.execute_insert(insert_sql, values)
            post_lst.append(post)
            counter+=1
            self.randSleep([60,95])
        return post_lst


INS = InsWrapper()
# INS.get_postsByUsername("nasa", 1)
INS.get_UserData(["minecraft"], "top", 10)