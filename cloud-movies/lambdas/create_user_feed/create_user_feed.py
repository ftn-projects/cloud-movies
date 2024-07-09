import boto3
import os
from boto3.dynamodb.conditions import Key
import json


video_types = ['MOVIE', 'SHOW']

dynamodb = boto3.resource('dynamodb')


def handler(event, context):
    feeds_table_name = os.environ['FEEDS_TABLE']
    videos_table_name = os.environ['VIDEOS_TABLE']

    feeds_table = dynamodb.Table(feeds_table_name)
    videos_table = dynamodb.Table(videos_table_name)

    message_str = event['Records'][0]['Sns']['Message']
    message_json = json.loads(json.loads(message_str)['default'])
    user_id = message_json['request']['userAttributes']['sub']

    for video_type in video_types:
        response = videos_table.query(KeyConditionExpression=Key('videoType').eq(video_type))
        for item in response['Items']:
            feeds_table.put_item(Item={
                'userId': user_id,
                'contentId': item['videoId'],
                'rating': 50 
            })
