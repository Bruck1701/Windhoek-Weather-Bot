# -*- coding: utf-8 -*-
import config
import tweepy
import datetime
from  SensorProducer import ArduinoSensor
import schedule
import time
import requests
import logging



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
        self.showData(self.arduino.ReadInput(),True)

    def job2(self):
        '''
        job that stores the data on a CSV File to be used to train a prediction model.
        '''
        pass

    def getJoke(self):
        '''
        Fetches a random joke to insert in the Tweet if the information about the weather and the joke is less than 280 chars.
        '''

        url = config.JOKE_API_URL

        response = requests.get(url)

        #print(response.json())
        if response.json()["type"]=="twopart":
            return response.json()["setup"]+"\n"+response.json()["delivery"]
        elif response.json()["type"]=="single":
            return  response.json()["joke"]

            return ""




    def showData(self,data,postTweet=False):
        '''
        Prints and tweets the collected data from the adaFruit Sensors.
        '''
        logging.basicConfig(filename='wwbot.log', level=logging.ERROR)

        degree_sign= u'\N{DEGREE SIGN}'
        info=f"[Namibia/Windhoek]: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\tCurrent Temperature: {data['Temp']}{degree_sign}, Humidity: {data['Hum']}%\nCaptured IR: {data['IR']}, Visible Light: {data['Vis']}"

        try:
            joke = self.getJoke()
            if len(info)+2+len(joke)<280:
                info +="\n\n"+joke
        except Exception:
            logging.exception("message")
        except OSError as e:
            logging.exception("message")

        finally:

            if postTweet:
                self.api.update_status(info)
            print(info)



if __name__ == "__main__":

    #job1()
    bot = WeatherBot()
    bot.job1()

    schedule.every(6).hours.do(bot.job1)


    while 1:
        schedule.run_pending()
        time.sleep(1)
