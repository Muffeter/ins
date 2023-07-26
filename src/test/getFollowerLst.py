import sys, os
current_dir = os.path.dirname(os.path.abspath(__file__))
api_path = os.path.join(current_dir, '..', 'api')
sys.path.append(api_path)
from bot import Bot, PleaseWaitFewMinutes, ClientError
from requests import HTTPError
import time, csv

bot = Bot()
print("finish login")
keyword = ["UGC","Makeup","Skincare"]
lst = bot.getMedia("glasses", amount=100)
print("finish getMedia")
try:
    user_pklst = (bot.getUser(l) for l in lst if Bot.getFollower_count(bot.getUser(l)) > 1000)
except Exception as e:
    print(e)
with open("data.csv", "w+",  encoding='utf-8') as f:
    csvf = csv.writer(f)
    csvf.writerow(['index', 'id', 'username', 'full_name', 'follower_count', 'media_count', 'email'])
    pos = 0
    while True:
        assert user_pklst
        try:
            print("[Writer]: Start writing")
            for _, user_pk in enumerate(user_pklst, pos):
                time.sleep(5)
                index = pos + 1
                print(f"writing {index}\n")
                csvf.writerow([index, user_pk.pk, user_pk.username, user_pk.full_name, user_pk.follower_count, user_pk.media_count, user_pk.public_email])
                pos += 1
            break
                
        except (PleaseWaitFewMinutes, HTTPError, ClientError) as e:
            print(e)
            print("Detected pause for 1 min")
            time.sleep(60)
            print("Start to crawl")
            continue
        except StopIteration:
            break
        except Exception as e:
            raise e
        