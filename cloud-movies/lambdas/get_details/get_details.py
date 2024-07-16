import json
import os
import boto3
import utils
from boto3.dynamodb.conditions import Key

video_types = ['SHOW', 'MOVIE']

def handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    
    table_name = os.getenv('VIDEOS_TABLE')
    table = dynamodb.Table(table_name)
    
    video_id = event['pathParameters']['videoId']
    for video_type in video_types:
        response = table.query(
            KeyConditionExpression=Key('videoId').eq(video_id) & Key('videoType').eq(video_type),
            ProjectionExpression='videoType,actors,videoId,title,directors,releaseDate,description,#time,genres',
            ExpressionAttributeNames={"#time": "duration"},
        )
        
        if 'Items' in response:
            items = response.get('Items', [])
            print(items)
            for item in items:
                print(item)
                if item.get('videoType') in ['SHOW', 'MOVIE']:
                    print('AAAA')
                    item['actors'] = item['actors'].split(',')
                    item['directors'] = item['directors'].split(',')
                    item['genres'] = item['genres'].split(',')
                    return utils.create_response(200, item)
        else:
            status_code = 404
            body = {'error': 'Item not found'}
            return utils.create_response(status_code, body)
    return utils.create_response(400, 'Error')