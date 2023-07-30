import sys, os
current_dir = os.path.dirname(os.path.abspath(__file__))
api_path = os.path.join(current_dir, '..', 'api')
sys.path.append(api_path)
from bot import Bot, PleaseWaitFewMinutes, ClientError
from requests import HTTPError
import csv

CSV_PATH = "./data/users.csv"

bot = Bot()
print("finish login")

keyword = ["UGC","Makeup","Skincare"]
lst = bot.getMedia(keyword, amount=100)
print("finish getMedia")

num = 0
try:
    with open(CSV_PATH, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["用户名","昵称","邮箱","粉丝数","主页链接"])
        
    for l in lst:
        user = bot.getUser(l)
        if l.getFollower_count(user) > 100:
            num += 1
            userName = Bot.getUsername(user)
            email = Bot.getEmail(user)
            fullName = Bot.getFullName(user)
            homeLink = Bot.getUserLink(user)
            follower_count = Bot.getFollower_count(user)
            
            newrow = [userName, fullName, email, follower_count, homeLink]
            with open(CSV_PATH, mode="a", newline="") as file:
                writer = csv.writer(file)
                file.write("\n")
                writer.writerow(newrow)
except:
    pass

print(num)