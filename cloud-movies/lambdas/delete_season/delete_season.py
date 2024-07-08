import json
import os
import boto3
from botocore.config import Config
from boto3.dynamodb.conditions import Key


def handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    s3 = boto3.client('s3', config=Config(signature_version='s3v4'))

    table_name = os.getenv('VIDEOS_TABLE')
    bucket_name = os.getenv('PUBLISH_BUCKET')
    table = dynamodb.Table(table_name)

    show_id = json.loads(event['pathParameters']['showId'])
    season = json.loads(event['pathParameters']['season'])
    
    response = table.query(
        KeyConditionExpression=Key('videoId').eq(show_id) & Key('videoType').begins_with(f'SHOW::S{season:02d}')
    )

    episodes = response['Items']
    filtered_episodes = [item for item in episodes if 'E' in item['videoType']]

    resolutions = ['360', '480', '720']

    for ep,resolution in zip(filtered_episodes, resolutions):
        video_file = ep['files'][resolution]['path']
        s3.Object(bucket_name, video_file).delete()

    for show in response:
        key = {'videoId': show_id, 'videoType': show['videoType']}
        table.delete_item(Key=key)

    return { 
        'statusCode': 204, 
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps({}, default=str)
    }