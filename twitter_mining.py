import requests_oauthlib
import configparser

'''
In order to access Twitter Streaming API, we need to get 4 pieces of information from Twitter: API key, API secret, Access token and Access token secret.
Follow the steps below to get all 4 elements:
	1. Create a twitter account if you do not already have one.
	2. Go to https://apps.twitter.com/ and log in with your twitter credentials.
	3. Click "Create New App"
	4. Fill out the form, agree to the terms, and click "Create your Twitter application"
	5. In the next page, click on "API keys" tab, and copy your "API key" and "API secret".
	6. Scroll down and click "Create my access token", and copy your "Access token" and "Access token secret".

Twitter API Docs:
https://dev.twitter.com/rest/reference

To retrieve different information, the request_url and params have to be changed according to the docs.
'''

config = configparser.ConfigParser()
config.read('twitterapi.cfg')
consumer_key = config.get('configuration', 'consumer_key')
consumer_secret = config.get('configuration', 'consumer_secret')
access_token = config.get('configuration', 'access_token')
access_token_secret = config.get('configuration', 'access_token_secret')


def tweet_text_by_id(screen_name, consumer_key, consumer_secret, access_token, access_token_secret):
    """
    Get the text of the most recent tweet.

    Args:
        screen_name (str): twitter account handle.
        consumer_key (str): Twitter API Consumer Key
        consumer_secret (str): Twitter API Consumer Secret
        access_token (str): Twitter API Access Token
        access_token_secret (str): Twitter API Access Token Secret

    Returns:
        str: The text of the specified tweet.

    """
    CONSUMER_KEY = consumer_key #API KEY
    CONSUMER_SECRET = consumer_secret #API SECRET

    twitter = requests_oauthlib.OAuth1Session(CONSUMER_KEY,
                            client_secret=CONSUMER_SECRET,
                            resource_owner_key=access_token,
                            resource_owner_secret=access_token_secret)

    request_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    params = {
    	'screen_name': screen_name
    }
    response = twitter.get(request_url, params=params)
    return response.json()[0]['text']


screen_name = '20thcenturyfox'
print(tweet_text_by_id(screen_name, consumer_key, consumer_secret, access_token, access_token_secret))


