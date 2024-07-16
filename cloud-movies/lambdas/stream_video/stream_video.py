import os
import boto3
from boto3.dynamodb.conditions import Key
import json
import utils
from botocore.config import Config
PRESIGNED_URL_EXPIRATION = 1 * 5 * 60  # hours

s3 = boto3.client('s3', config=Config(s3={'addressing_style': 'path'}, signature_version='s3v4', region_name='eu-central-1'))
dynamo = boto3.resource('dynamodb')

video_types = ['MOVIE', 'SHOW']

def handler(event, context):
    table_name = os.getenv('VIDEOS_TABLE')
    bucket_name = os.getenv('PUBLISH_BUCKET')

    video_id = event['pathParameters']['videoId']
    resolution = event['pathParameters']['resolution']
    
    
    table = dynamo.Table(table_name)
    item = find_content(table_name, video_id)
    video_file = ''
    print(item)
    video_type = item.get('videoType', '')
    if video_type == 'MOVIE':
        video_file = find_movie(item, resolution)
    elif video_type == 'TV_SHOW':
        season = event['queryStringParameters'].get('season', '')
        episode = event['queryStringParameters'].get('episode', '')
        video_file = find_episode(season, episode, table, video_id, resolution)

    if video_file == '':
        return utils.create_response(400,'Episode not found')
    
    url = s3.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': bucket_name, 
            'Key': video_file,
        },
        ExpiresIn=PRESIGNED_URL_EXPIRATION
    )
    return utils.create_response_presigned_link(200, url)

def find_episode(season, episode, table, video_id, resolution):
    if season != '' and episode != '':
        season_num = int(season)
        episode_num = int(episode)
        response2 = table.query(Key={'videoId':video_id, 'videoType': f'SHOW::S{season_num:02d}::E{episode_num:02d}'}) 
        if 'Item' not in response2:
           return '' 
        return response2['Item']['files'][resolution]['path']

def find_movie(item, resolution):
    return item['files'][resolution]['path']

def find_content(table_name, video_id):
    table = dynamo.Table(table_name)
    for video_type in video_types:
        response = table.get_item(Key={
                'videoId': video_id,
                'videoType': video_type
                 })
    
        if 'Item' in response:
            return response['Item']
    