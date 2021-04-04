import os
import json
import sys
import geocoder
import tweepy
from collections import OrderedDict


class TweepyIntegration(object):
    def __init__(self):
        self.consumer_key = '2NRaJjiOUmYJ4dbB2zS7235VH'
        self.consumer_secret = 'Haf4MsVQBcum41Oz4Zp1g6irlgOudfS7xkHvwUqfLebI8gpvRD'
        self.authentication()

    def authentication(self):
        auth = tweepy.AppAuthHandler(self.consumer_key, self.consumer_secret)
        self.api = tweepy.API(auth)
        return True
 
    def get_trending(self):
        # Trends for Specific Country
        loc = 'india'   # location as argument variable 
        g = geocoder.osm(loc) # getting object that has location's latitude and longitude

        closest_loc = self.api.trends_closest(g.lat, g.lng)
        trends = self.api.trends_place(closest_loc[0]['woeid'])

        # writing a JSON file that has the latest trends for that location
        with open("twitter_{}_trend.json".format(loc),"w") as wp:
            wp.write(json.dumps(trends, indent=4))

        return True

    def get_tweets(self, search_words, retweet=True, number_of_tweets=10):
        if not retweet:
            search_words = search_words + " -filter:retweets"

        tweets = tweepy.Cursor(self.api.search, 
            q=search_words,
            lang="en",
            since="2020-01-01"
        ).items(number_of_tweets)
        
        tweet_list = []
        for tweet in tweets:
            tweet_dict = OrderedDict()
            tweet_dict['user_name'] = tweet.user.screen_name
            tweet_dict['location'] = tweet.user.location
            tweet_dict['text'] = tweet.text
            tweet_list.append(tweet_dict)

        return tweet_list

if __name__ == "__main__":
    obj = TweepyIntegration()
    print(obj.get_tweets('corona', False))
