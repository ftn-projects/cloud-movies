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
    
    show_id = json.loads(event['pathParameters']['showId'])
    season = json.loads(event['pathParameters']['season'])
    episode = json.loads(event['pathParameters']['episode'])
    value = event['body']

    key = {'videoId': show_id, 'videoType': f'SHOW::S{season:02d}::E{episode:02d}'}
    response = table.get_item(Key=key)

    if 'Item' in response:
        item = response['Item']

        for param in ['title', 'description', 'releaseDate']:
            item[param] = value[param]

        item['modified_at'] = datetime.now().isoformat()

        table.put_item(Item=item)
        status_code = 200
        body = item
    else:
        status_code = 404
        body = {'error': 'Item not found'}

    return utils.create_response(status_code, body)