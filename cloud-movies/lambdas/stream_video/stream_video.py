import os
import boto3
import botocore
import json
import utils
from botocore.config import Config
PRESIGNED_URL_EXPIRATION = 1 * 5 * 60  # hours

s3 = boto3.client('s3', config=Config(s3={'addressing_style': 'path'}, signature_version='s3v4', region_name='eu-central-1'))
dynamo = boto3.resource('dynamodb')

def handler(event, context):
    table_name = os.getenv('VIDEOS_TABLE')
    bucket_name = os.getenv('PUBLISH_BUCKET')

    video_id = event['pathParameters']['videoId']
    video_type = event['pathParameters']['videoType']
    resolution = event['pathParameters']['resolution']

    table = dynamo.Table(table_name)
    response = table.get_item(Key={'videoId': video_id, 'videoType': video_type})
    print(response)
    if 'Item' not in response:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Video not found'})
        }
     
    video_file = response['Item']['files'][resolution]['path']
    print(video_file)
    print(bucket_name, video_file)
    url = s3.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': bucket_name, 
            'Key': video_file,
        },
        ExpiresIn=PRESIGNED_URL_EXPIRATION
    )
    print(url)
    response = s3.get_object(Bucket=bucket_name, Key=video_file)
    print(response)
    return utils.create_response_presigned_link(200, url)
