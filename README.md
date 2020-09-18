# Windhoek-Weather-Bot

![wwbot-face](https://user-images.githubusercontent.com/17711277/93581344-520f3280-f9a1-11ea-8570-be97a531e619.jpg)

This is a small pet project for a Python bot that collects raw data from an Arduino Board connected to RaspberryPi.
The bot also fetches data from OpenWeather and sends the sensor collected data and the API data to an SNS Topic in AWS.
<br>
The SNS Topic, then, triggers two Lambda functions: 
* A Lambda function that tweets the sensor data and the OpenWeather data. (<a href=https://twitter.com/BotWindhoek> @BotWindhoek </a>)
* Another lambda function that stores the sensor data into a DynamoDB table. 
<br>

The current flow of data in AWS:
![architecture](https://user-images.githubusercontent.com/17711277/93358773-2e81a600-f842-11ea-86c7-ac50a51f1625.jpg)


The next stage is to add another bot that gets the DynamoDB data and predicts the next reading from the sensor using LSTM Machine Learning model.

