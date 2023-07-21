import sys, os
current_dir = os.path.dirname(os.path.abspath(__file__))
api_path = os.path.join(current_dir, '..', 'api')
sys.path.append(api_path)
from bot import Bot
bot = Bot()
lst = bot.getMedia("love", amount=10)
user_pklst = (bot.getUser(l) for l in lst if Bot.getFollower_count(bot.getUser(l)) > 10000)
for i in user_pklst:
    print(i)