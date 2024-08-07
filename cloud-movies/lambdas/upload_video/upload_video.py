import boto3
import uuid
import json
import os


PRESIGNED_URL_EXPIRATION = 1 * 60 * 60  # hours


def handler(event, context):
    s3_client = boto3.client('s3')
    bucket_name = os.environ['SOURCE_BUCKET']
    
    video_uuid = str(uuid.uuid4())  # will be used in dynamodb

    upload_url = s3_client.generate_presigned_post(
            Bucket=bucket_name,
            Key=f'{video_uuid}.zip',
            Fields = {
                "Content-Type": "application/zip"
            },
            Conditions = [
                {"Content-Type": "application/zip"}
            ],
            ExpiresIn = PRESIGNED_URL_EXPIRATION
    )

    return {
        'statusCode': 200,
        'body': json.dumps({'uploadUrl': upload_url}),
        'headers': {
            'Access-Control-Allow-Origin': '*',
        }
    }
