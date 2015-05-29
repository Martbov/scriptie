#!usr/bin/python3.4

#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json

#Variables that contains the user credentials to access Twitter API 
access_token = "3123623151-23vzgGPK9AEZZ9s6FJR2aEkjWFaeyFt5nWaA3VO"
access_token_secret = "31ZlYBMPTXZAJrYEqC2Yc1aplxwvegMjK0oHXQC33NqdL"
consumer_key = "BHX7KyZ47jOtDX67WFEb0l4u5"
consumer_secret = "hPISvGxAGfBadwf5ZHYObNzc7mIETahMMLY2tVwZwXJSNxa01Q"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        decoded = json.loads(data)
        print('@%s: %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore')))
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['#nedtur'])