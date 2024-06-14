import os
import boto3


PRESIGNED_URL_EXPIRATION = 1 * 60 * 60  # hours


def handler(event, context):
    s3_client = boto3.client('s3')
    bucket_name = os.getenv('BUCKET_NAME')

    video_file = event['pathParameters']['video_file']
    
    download_url = s3_client.generate_presigned_url(
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
