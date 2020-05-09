# -*- coding: utf-8 -*-
import config
import tweepy
import datetime
from  SensorProducer import ArduinoSensor



API_PUBLIC = config.API_KEY
API_SECRET = config.API_SECRET_KEY
ACCESS_TOKEN = config.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = config.ACCESS_TOKEN_SECRET

auth = tweepy.OAuthHandler(API_PUBLIC, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)



def showData(Data):
    degree_sign= u'\N{DEGREE SIGN}'
    info=f"[Namibia/Windhoek]: {datetime.datetime.now()}\n\tCurrent Temperature: {Data['Temp']}{degree_sign}, Humidity: {Data['Hum']}\n\
\tCaptured IR: {Data['IR']}, Visible Light: {Data['Vis']}"

    #api.update_status(info)
    print(info)


arduino = ArduinoSensor()
showData(arduino.ReadInput())
