# -*- coding: utf-8 -*-
import config
import tweepy
import datetime
from  SensorProducer import ArduinoSensor
import schedule
import time

class WeatherBot():

    API_PUBLIC = config.API_KEY
    API_SECRET = config.API_SECRET_KEY
    ACCESS_TOKEN = config.ACCESS_TOKEN
    ACCESS_TOKEN_SECRET = config.ACCESS_TOKEN_SECRET

    def __init__(self):
        self.auth = tweepy.OAuthHandler(self.API_PUBLIC, self.API_SECRET)
        self.auth.set_access_token(self.ACCESS_TOKEN, self.ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(self.auth)
        self.arduino = ArduinoSensor()


    def job1(self):
        '''
        job that is schedule to tweet the data
        '''
        self.showData(self.arduino.ReadInput(),False)

    def job2(self):
        '''
        job that stores the data on a CSV File to be used to train a prediction model.
        '''
        pass


    def showData(self,data,postTweet=False):
        '''
        Prints and tweets the collected data from the adaFruit Sensors.
        '''
        degree_sign= u'\N{DEGREE SIGN}'
        info=f"[Namibia/Windhoek]: {datetime.datetime.now()}\n\tCurrent Temperature: {data['Temp']}{degree_sign}, Humidity: {data['Hum']}%\n \
        Captured IR: {data['IR']}, Visible Light: {data['Vis']}"
        #info = " [Namibia/Windhoek]: {}".format(datetime.datetime.now())

        if postTweet:
            self.api.update_status(info)
        print(info)



if __name__ == "__main__":

    bot = WeatherBot()

    schedule.every(3).minutes.do(bot.job1)


    while 1:
        schedule.run_pending()
        time.sleep(1)
