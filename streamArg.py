import io
import os
import time
import json
import sys
import tweepy
import csv
from tweepy.auth import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from config import *

class listener(StreamListener):

    def __init__(self, start_time, time_limit=60):
        self.time = start_time
        self.limit = time_limit
        self.tweet_data = []
        self.begin = time.asctime( time.localtime(time.time()) )
    
    def on_data(self, data):
        # stream data sampai waktu yang ditentukan (time_limit)
        while (time.time() - self.time) < self.limit:

            try:
                data_append = {}
                data_dict = json.loads(data)
                # print(data_dict["text"])
                print("--")
                data_append["hashtags"] = ""
                for item in data_dict["entities"]["hashtags"]:
                    # print(item["text"])
                    data_append["hashtags"] += str(item["text"]) + ", "
                data_append["text"] = data_dict["text"]
                self.tweet_data.append(data_append)
                return True
            except BaseException as e:
                print('failed ondata', str(e))
                time.sleep(5)
                pass
        csv_head = ['text', 'hashtags'] #csv head
        csv_name = self.begin +' - ' + time.asctime( time.localtime(time.time()) )+ ".csv"

        try:
            with open(sys.argv[2] + "/" + csv_name, 'w') as csv_name:
                writer = csv.DictWriter(csv_name, fieldnames=csv_head)
                writer.writeheader()
                for data in self.tweet_data:
                    writer.writerow(data)
        except IOError:
                print("I/O error")
        exit()

    def on_error(self, status):
        print(status)


auth = OAuthHandler(ckey, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
api = tweepy.API(auth)

trends = api.trends_place(23424846)
top10trends = []
for i in range(10):
    top10trends.append(trends[0]["trends"][i]["name"])
print(top10trends)

start_time = time.time()
minute = int(sys.argv[1]) * 60
twitterStream = Stream(auth, listener(start_time, time_limit=minute))
twitterStream.filter(track=top10trends, async=True)
