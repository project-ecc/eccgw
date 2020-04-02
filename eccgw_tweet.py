import tweepy

import settings

################################################################################

def sendTweet(handle = '', content = ''):

    auth = tweepy.OAuthHandler(settings.twitter_api_key, settings.twitter_api_secret_key)

    auth.set_access_token(settings.twitter_access_token, settings.twitter_access_token_secret)

    api = tweepy.API(auth)

    api.update_status(status ="%s %s" % (handle, content))