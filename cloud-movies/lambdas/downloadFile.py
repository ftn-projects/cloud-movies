import os
import json
import boto3
from botocore.exceptions import ClientError

dynamodb_client = boto3.client('dynamodb')
s3_client = boto3.client('s3', region_name='eu-central-1')


def download_file_handler(event, context):
    table_name = os.getenv('TABLE_NAME')
    bucket_name = os.getenv('BUCKET_NAME')

    if table_name is None or bucket_name is None:
        raise ValueError('Missing environment variable')


    try:
        response = dynamodb_client.scan(TableName=table_name)
        files = response.get('Items', [])

    except ClientError as e:
        print(e.response['Error']['Message'])
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error'}),
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
        }


    files_with_presigned_urls = []
    # Generate pre-signed URLs for each file
    for item in files:
        print(item)
        file_name = item.get('id', {}).get('S')

        if file_name:
            download_url = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': f"{file_name}"},
                ExpiresIn=3600
            )
            files_with_presigned_urls.append({
                'fileName': file_name,
                'downloadUrl': download_url
            })

    return {
        'statusCode': 200,
        'body': json.dumps({'files': files_with_presigned_urls}),
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
    }
