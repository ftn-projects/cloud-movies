import os
import boto3
import json


PRESIGNED_URL_EXPIRATION = 1 * 60 * 60  # hours

dynamo = boto3.resource('dynamodb')
s3 = boto3.client('s3')


def handler(event, context):
    table_name = os.getenv('VIDEOS_TABLE')
    bucket_name = os.getenv('PUBLISH_BUCKET')

    video_id = event['pathParameters']['videoId']
    video_type = event['pathParameters']['videoType']
    resolution = event['pathParameters']['resolution']

    table = dynamo.Table(table_name)
    response = table.get_item(Key={'videoId': video_id, 'videoType': video_type})

    if 'Item' not in response:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Video not found'})
        }
    
    video_file = response['Item']['file'][resolution]['path']
    print(video_file)

    download_url = s3.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': bucket_name, 
            'Key': video_file
        },
        ExpiresIn=PRESIGNED_URL_EXPIRATION
    )

    return {
        'statusCode': 307,
        'headers': {
            'Location': download_url
        }
    }
