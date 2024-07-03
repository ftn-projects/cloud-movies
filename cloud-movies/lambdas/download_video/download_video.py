import os
import boto3
import json


PRESIGNED_URL_EXPIRATION = 1 * 60 * 60  # hours


def handler(event, context):
    dynamo = boto3.resource('dynamodb')
    s3 = boto3.client('s3')

    table_name = os.getenv('VIDEOS_TABLE')
    bucket_name = os.getenv('SOURCE_BUCKET')

    video_id = event['pathParameters']['video_id']
    resolution = event['pathParameters']['resolution']
    print(video_id)

    table = dynamo.Table(table_name)
    response = table.get_item(Key={'id': video_id})

    if 'Item' not in response:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Video not found'})
        }
    
    video_file = response['Item']['files'][resolution]['path']
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
