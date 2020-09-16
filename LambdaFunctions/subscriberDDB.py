import json
import boto3
import time
import os
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):

    ts = time.time()
    message_attrs = event['Records'][0]['Sns']['MessageAttributes']
    print(ts)
    print(message_attrs)
    delta = 2592000 # ts+delta: 30 days from today

    response = table.put_item(
          Item={
                'timestamp': Decimal(str(ts)),
                'expire_on': Decimal(str(ts+delta)),
                'datetime': message_attrs['datetime']['Value'],
                'temp': Decimal(message_attrs['temp']['Value']),
                'hum':  Decimal(message_attrs['hum']['Value']),
                'ir':   Decimal(message_attrs['ir']['Value']),
                'vis':  Decimal(message_attrs['vis']['Value'])
                }
        )

    return 0
