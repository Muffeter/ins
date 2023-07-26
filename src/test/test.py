import sys, os
current_dir = os.path.dirname(os.path.abspath(__file__))
api_path = os.path.join(current_dir, '..', 'api')
sys.path.append(api_path)
from bot import Bot, PleaseWaitFewMinutes, ClientError
from requests import HTTPError

bot = Bot()
print("finish login")
keyword = ["UGC","Makeup","Skincare"]
lst = bot.getMedia(keyword, amount=100)
print("finish getMedia")
num = 0
try:
    for l in lst:
        if Bot.getFollower_count(bot.getUser(l)) > 100:
            num += 1
except:
    pass
print(num) 