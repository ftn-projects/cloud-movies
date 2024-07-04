import boto3
import json
import os

def handler(event, context):
    s3 = boto3.client('s3')
    dynamodb = boto3.client('dynamodb')
    table_name = os.getenv('VIDEOS_TABLE')
    
    s3_bucket = event['Records'][0]['s3']['bucket']['name']
    s3_key = event['Records'][0]['s3']['object']['key']

    try:
        table = dynamodb.Table(table_name)
        response = table.get_item(Key={'id': s3_key})
        
        if 'Item' in response:
            print(f'Item {s3_key} is found in {table_name}')
        else:
            s3.delete_object(Bucket=s3_bucket, Key=s3_key)

    except Exception as e:
        print(f"Error: {str(e)}")
        raise e