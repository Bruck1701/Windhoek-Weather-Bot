import config
import tweepy
import datetime
from  SensorReader import ArduinoSensor
import requests
import boto3


def getWeatherDataAPI():
    temp_data={}
    url = "https://api.openweathermap.org/data/2.5/weather?q=Windhoek,na&appid="+config.WEATHER_API
    response = requests.get(url)
    if "main" in response.json():
        temp_data["temp"]=   "{:.2f}".format((float(response.json()["main"]["temp"])- 273.15))
        temp_data["pressure"] = response.json()["main"]["pressure"]
        temp_data["humidity"] = response.json()["main"]["humidity"]
        return temp_data
    return None

if __name__ == "__main__":
    arduino = ArduinoSensor()
    data = arduino.ReadInput()
    api_data = getWeatherDataAPI()
    info = ""
    degree_sign= u'\N{DEGREE SIGN}'

    msg=f"[Windhoek/NA]: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nSensor_Temp: {data['Temp']}{degree_sign}, Humidity: {data['Hum']}%\nCaptured_IR: {data['IR']}, Visible_Light: {data['Vis']}\n"
    msg+=f"\nOpenWeather_data: Temp: {api_data['temp']}{degree_sign}, Hum: {api_data['humidity']}%, Press: {api_data['pressure']}"

    client = boto3.client('sns')

    response = client.publish(
    TopicArn=config.TOPIC_ARN,
    Message=msg,
    Subject='Weather Data',
     MessageAttributes={
        'datetime': {
            'DataType': 'String',
            'StringValue': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        'temp': {
            'DataType': 'String',
            'StringValue': str(data['Temp'])
        },
        'hum': {
            'DataType': 'String',
            'StringValue': str(data['Hum'])
        },
        'ir': {
            'DataType': 'String',
            'StringValue': str(data['IR'])
        },
        'vis': {
            'DataType': 'String',
            'StringValue': str(data['Vis'])
        }
        }

    )

    print(response)
