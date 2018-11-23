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
from model.sentiment import *
from config import * 

global graph
graph = tf.get_default_graph()
vocab, tokenizer, max_length, model = load_variabels()

class listener(StreamListener):

    def __init__(self, start_time, time_limit=60, directory='/file/'):
        self.time = start_time
        self.limit = time_limit
        self.tweet_data = []
        self.begin = time.asctime( time.localtime(time.time()) )
        self.end = ''
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

        
        for i in range(1):
            self.end = time.asctime( time.localtime(time.time()) )
            print(self.end)

        with open(self.directory + "/" + self.begin + ' - ' +  self.end, 'w') as f:
            for item in self.tweet_data:
                item = item.replace('\n','')
                f.write("%s\n" % item)
        
        # Predict model
        input_file = open(raw_file_directory + "/" + self.begin + ' - ' +  self.end )
        csv_head = ['text', 'conclusi', 'percent']
        csv_body = []
        for line in input_file:
            with graph.as_default():
                percent, conclusion = predict_sentiment(line, vocab, tokenizer, max_length, model)
            csv_line = {}
            csv_line["text"] = line
            csv_line["conclusi"] = conclusion
            csv_line["percent"] = str(percent * 100)
            csv_body.append(csv_line)
        
        input_file.close()
        print(csv_body)
        # os.remove(raw_file_directory + "/" + filename)

        csv_name = self.begin + ' - ' +  self.end + ".csv"
        try:
            with open(predict_file_directory + "/" + csv_name, 'w') as csv_name:
                writer = csv.DictWriter(csv_name, fieldnames=csv_head)
                writer.writeheader()
                for data in csv_body:
                    writer.writerow(data)
        except IOError:
                print("I/O error")
        exit()

    def on_error(self, status):
        print(status)


auth = OAuthHandler(ckey, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
api = tweepy.API(auth)

def begin_stream_automatic(second, directory):
    minute = second * 60
    trends = api.trends_place(23424846)
    top10trends = []
    for i in range(10):
        top10trends.append(trends[0]["trends"][i]["name"])
    print(top10trends)

    start_time = time.time()
    twitterStream = Stream(auth, listener(start_time, time_limit=minute, directory=directory))
    twitterStream.filter(track=top10trends, async=True)


# begin_stream(1, dir_aplikasi + "/" +raw_file_directory)