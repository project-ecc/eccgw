import tweepy

import settings

################################################################################

def sendTweet(handle = '', content = ''):

    consumer_key        = ""
    consumer_secret     = ""
    access_token        = ""
    access_token_secret = ""

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    api.update_status(status ="%s %s" % (handle, content))