import json
import os
import boto3


def handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    
    table_name = os.getenv('TABLE_NAME')
    table = dynamodb.Table(table_name)
    
    item_id = json.loads(event['pathParameters']['video_id'])
    
    key = {'id': item_id}
    
    response = table.get_item(Key=key)
    
    if 'Item' in response:
        item = response['Item']
        status_code = 200
        body = json.dumps(item)
    else:
        status_code = 404
        body = json.dumps({'error': 'Item not found'})
    
    return {
        'statusCode': status_code,
        'body': body
    }