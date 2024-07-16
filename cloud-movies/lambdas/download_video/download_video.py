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

    download_url = s3.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': bucket_name, 
            'Key': video_id
        },
        ExpiresIn=PRESIGNED_URL_EXPIRATION
    )

    return {
        'statusCode': 307,
        'headers': {
            'Location': download_url
        }
    }
