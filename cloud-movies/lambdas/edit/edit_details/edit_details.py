import datetime
import json
import os
import boto3
import utils
from botocore.config import Config

def handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    s3 = boto3.client('s3', config=Config(signature_version='s3v4'))

    table_name = os.getenv('VIDEOS_TABLE')
    table = dynamodb.Table(table_name)
    
    video_id = json.loads(event['pathParameters']['videoId'])
    video_type = json.loads(event['pathParameters']['videoType'])
    value = event['body']

    key = {'videoId': video_id, 'videoType': video_type}
    response = table.get_item(Key=key)

    if 'Item' in response:
        item = response['Item']

        for param in ['title', 'description', 'releaseDate', 'genres', 'actors', 'directors']:
            item[param] = value[param]

        item['modified_at'] = datetime.now().isoformat()

        table.put_item(Item=item)
        status_code = 200
        body = item
    else:
        status_code = 404
        body = {'error': 'Item not found'}

    return utils.create_response(status_code, body)