# -*- coding: utf-8 -*-
import config
import tweepy
import datetime
from  SensorProducer import ArduinoSensor
import schedule
import time
import requests
import logging
import threading



class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        pass
        #print(status.text)

    def on_error(self, status):
        pass
        #print(status)




class WeatherBot:

    API_PUBLIC = config.API_KEY
    API_SECRET = config.API_SECRET_KEY
    ACCESS_TOKEN = config.ACCESS_TOKEN
    ACCESS_TOKEN_SECRET = config.ACCESS_TOKEN_SECRET

    def __init__(self):
        self.auth = tweepy.OAuthHandler(self.API_PUBLIC, self.API_SECRET)
        self.auth.set_access_token(self.ACCESS_TOKEN, self.ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(self.auth)

        myStreamListener = MyStreamListener()
        myStream = tweepy.Stream(auth = self.api.auth, listener=myStreamListener)
        #myStream.filter(follow=[config.Bruck_ID],is_async=True)
        myStream.filter(follow=[config.bot_ID],is_async=True)



    def job1(self):
        '''
        job that is schedule to tweet the data
        '''
        arduino = ArduinoSensor()
        data = arduino.ReadInput()
        weather_api_data = self.getWeatherDataAPI()
        self.showData(data,weather_api_data,True)


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
        if "type" in response.json():
            if response.json()["type"]=="twopart":
                return response.json()["setup"]+"\n"+response.json()["delivery"]
            elif response.json()["type"]=="single":
                return  response.json()["joke"]
        return ""


    def getWeatherDataAPI(self):
        temp_data={}
        url = "https://api.openweathermap.org/data/2.5/weather?q=Windhoek,na&appid="+config.WEATHER_API
        response = requests.get(url)
        if "main" in response.json():
            temp_data["temp"]= str(float(response.json()["main"]["temp"])- 273.15)
            temp_data["pressure"] = response.json()["main"]["pressure"]
            temp_data["humidity"] = response.json()["main"]["humidity"]
            return temp_data
        return None



    def showData(self,data,api_data,postTweet=False):
        '''
        Prints and tweets the collected data from the adaFruit Sensors.
        '''
        logging.basicConfig(filename='wwbot.log', level=logging.ERROR)

        degree_sign= u'\N{DEGREE SIGN}'
        info=f"[Windhoek/NA]: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nSensor Temp.: {data['Temp']}{degree_sign}, Humidity: {data['Hum']}%\nCaptured IR: {data['IR']}, Visible Light: {data['Vis']}"
        info+=f"\nOpenWeather data: Temp:{api_data['temp']}{degree_sign}, Hum:{api_data['humidity']}%, Press:{api_data['pressure']}"

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
            else:
                print(info)


    def thread_post_information(self):
        schedule.every(6).hours.do(self.job1)

        while 1:
            schedule.run_pending()
            time.sleep(2)


if __name__ == "__main__":
    bot = WeatherBot()
    bot.job1()

    x = threading.Thread(target=bot.thread_post_information)
    x.start()
