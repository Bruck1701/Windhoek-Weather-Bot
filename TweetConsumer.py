import json
import boto3
import tweepy

ssm = boto3.client('ssm',region_name='us-east-1')


def lambda_handler(event, context):

    params = ssm.get_parameters(Names=['/wwbot-app/dev/twitter/api_key',
                    '/wwbot-app/dev/twitter/api_secret_key',
                    '/wwbot-app/dev/twitter/access_token',
                    '/wwbot-app/dev/twitter/access_token_secret'], WithDecryption=True)['Parameters']


    access_token = params[0]['Value']
    access_token_secret = params[1]['Value']
    api_key = params[2]['Value']
    api_secret_key = params[3]['Value']
    
    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    con = tweepy.API(auth)

    message = event['Records'][0]['Sns']['Message']

    con.update_status("☁️ "+message)

    return 0
