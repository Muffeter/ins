from ins import Ins
import json
import config_my
# from gui import GUI

# you must have your login cookie
COOKIE = config_my.cookie
JSON_PATH = "./data.json"


INS = Ins(COOKIE)
# gui = GUI()
username_lst = INS.getUserBytag("minecraft", "top")
for username in username_lst:
    print(INS.get_userInfo(username))
    with open(JSON_PATH, "a") as json_file:
        json.dump(INS.get_userInfo(username), json_file)
    INS.randSleep([60,95])
    
print("hello world")