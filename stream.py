import io
import os
import time
import json
import sys
import tweepy
from tweepy.auth import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from config import *

class listener(StreamListener):

    def __init__(self, start_time, time_limit=60, directory='/file/'):
        self.time = start_time
        self.limit = time_limit
        self.tweet_data = []
        self.begin = time.asctime( time.localtime(time.time()) )
        self.directory = directory
    
    def on_data(self, data):
        # stream data sampai waktu yang ditentukan (time_limit)
        while (time.time() - self.time) < self.limit:

            try:
                data_dict = json.loads(data)
                print(data_dict["text"])
                self.tweet_data.append(data_dict["text"])
                return True
            except BaseException as e:
                print('failed ondata', str(e))
                time.sleep(5)
                pass

        with open(self.directory + "/" + self.begin +' - ' + time.asctime( time.localtime(time.time()) ), 'w') as f:
            for item in self.tweet_data:
                item = item.replace('\n','')
                f.write("%s\n" % item)
        exit()

    def on_error(self, status):
        print(status)


auth = OAuthHandler(ckey, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
api = tweepy.API(auth)

def begin_stream_manual(second, directory):
    minute = second * 60
    trends = api.trends_place(23424846)
    top10trends = []
    for i in range(10):
        top10trends.append(trends[0]["trends"][i]["name"])
    print(top10trends)

    start_time = time.time()
    twitterStream = Stream(auth, listener(start_time, time_limit=minute, directory=directory))
    twitterStream.filter(track=top10trends, async=True)


begin_stream_manual(1, dir_aplikasi + "/" +raw_file_directory)
