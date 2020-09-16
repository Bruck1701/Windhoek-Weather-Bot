# Windhoek-Weather-Bot

This is a project for a Python bot that fetches raw data from an Arduino Board and stores the data and publishes it on Twitter (<a href=https://twitter.com/BotWindhoek> @BotWindhoek </a>)
<br>

In this new version, the bot fetches the data from the board and publishes it into an AWS SNS Topic. The topic, then,  triggers two lambda functions: 
* A Lambda function that tweets the sensor data and also Open Weather API data.
* Another lambda function that stores the sensor data into a DynamoDB table. 

The flow of data in AWS:
![architecture](https://user-images.githubusercontent.com/17711277/93358773-2e81a600-f842-11ea-86c7-ac50a51f1625.jpg)

The next stage is to add another bot that fetches the DynamoDB data and predicts the next reading from the sensor using LSTM model.

