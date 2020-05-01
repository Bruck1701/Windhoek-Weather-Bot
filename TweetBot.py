import config
import tweepy
import datetime



API_PUBLIC = config.API_KEY
API_SECRET = config.API_SECRET_KEY
ACCESS_TOKEN = config.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = config.ACCESS_TOKEN_SECRET

auth = tweepy.OAuthHandler(API_PUBLIC, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

def publictweet():
    string_header="This is a bot test... "

    if datetime.date.today().weekday() == 0:
        tweettopublish = 'Hi everyone, today is Monday.   #Monday '
    if datetime.date.today().weekday() == 1:
        tweettopublish = 'Enjoy your Tuesday.  #Tuesday'
    if datetime.date.today().weekday() == 2:
        tweettopublish = 'Third week of the Week. #Wednesday'
    if datetime.date.today().weekday() == 3:
        tweettopublish = 'Thursday. I cannot wait for the Weekend'
    if datetime.date.today().weekday() == 4:
        tweettopublish = 'Friday...Finally'
    if datetime.date.today().weekday() == 5:
        tweettopublish = 'Great it is Saturday #weekend #Saturday'
    if datetime.date.today().weekday() == 6:
        tweettopublish = 'Sunday morning...#Weekend #enjoy '

    api.update_status(string_header+tweettopublish)
    print(tweettopublish)


publictweet()
