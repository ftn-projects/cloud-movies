import json
import os
import boto3
import utils
from botocore.config import Config

def handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    s3 = boto3.client('s3', config=Config(signature_version='s3v4'))

    table_name = os.getenv('VIDEOS_TABLE')
    bucket_name = os.getenv('PUBLISH_BUCKET')
    table = dynamodb.Table(table_name)
    
    video_id = json.loads(event['pathParameters']['videoId'])
    video_type = json.loads(event['pathParameters']['videoType'])
    
    key = {'videoId': video_id, 'videoType': video_type}
    table_response = table.get_item(Key=key)
    
    if 'Item' not in table_response:
        status_code = 404
        body = {'error': 'Item not found'}
        return utils.create_response(status_code, body)

    table.delete_item(Key=key)

    for resolution in ['360', '480', '720']:
        video_file = table_response['Item']['files'][resolution]['path']
        s3.Object(bucket_name, video_file).delete()

    return utils.create_response(204,'')