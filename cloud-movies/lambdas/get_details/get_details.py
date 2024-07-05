import json
import os
import boto3
import utils

def handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    
    table_name = os.getenv('VIDEOS_TABLE')
    table = dynamodb.Table(table_name)
    
    video_id = json.loads(event['pathParameters']['videoId'])
    video_type = json.loads(event['pathParameters']['videoType'])
    
    key = {'videoId': video_id, 'videoType': video_type}
    response = table.get_item(Key=key)
    
    if 'Item' in response:
        item = response['Item']
        status_code = 200
        body = item
    else:
        status_code = 404
        body = {'error': 'Item not found'}
    
    return utils.create_response(status_code, body)