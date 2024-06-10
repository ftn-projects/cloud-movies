import json
import os
import boto3
from botocore.exceptions import ClientError

dynamodb_client = boto3.client('dynamodb')
s3_client = boto3.client('s3')

def upload_file_handler(event, context):
    table_name = os.environ('TABLE_NAME')
    bucket_name = os.environ('BUCKET_NAME')

    if table_name is None or bucket_name is None:
        raise ValueError('Missing env variables')
    
    body = json.loads(event['body'])
    file_name = body.get('fileName')
    
    if file_name is None:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': 'Missing filename'
            }),
            'headers':{
                'Access-Control-Allow-Origin': '*'
            }
        }
    
    try:
        dynamodb_client.put_item(
            TableName=table_name,
            Item={
                'PK': {'S': file_name}
            }
        )
    except ClientError:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error'}),
            'headers': {
                'Access-Control-Allow-Origin': '*'
            }
        }
    
    try:
        upload_url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': bucket_name,
                'Key': f"/{file_name}"
            },
            ExpiresIn=60
        )
    except ClientError:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error'}),
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
        }
    
    return {
        'statusCode': 200,
        'body': json.dumps({'uploadUrl': upload_url}),
        'headers': {
            'Access-Control-Allow-Origin': '*'
        }
    }


