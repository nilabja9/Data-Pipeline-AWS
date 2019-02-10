import tweepy
from tweepy import OAuthHandler
import boto3
import json
import time
import twittercred
import awscred

auth = OAuthHandler(twittercred.consumerkey, twittercred.consumersecret)
auth.set_access_token(twittercred.accesskey, twittercred.accesssecret)

api = tweepy.API(auth)
topic = 'Donald Trump'

if __name__ == '__main__':

    client = boto3.client('firehose', aws_access_key_id = awscred.accesskey, aws_secret_access_key = awscred.accesssecret)

    while True:
        for tweet in tweepy.Cursor(api.search, q=topic).items(1000):
            response = client.put_record(
                DeliveryStreamName='kinesisnilabja',
                Record={
                    'Data': json.dumps(tweet._json) + '\n'
                }


            )
            print(response)




        time.sleep(300)


