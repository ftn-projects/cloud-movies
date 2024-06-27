import json
import os
import boto3


def handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    
    table_name = os.getenv('TABLE_NAME')
    table = dynamodb.Table(table_name)
    
    response = table.scan()
    items = response.get('Items', [])
    
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        items.extend(response.get('Items', []))

    return {
        'statusCode': 200,
        'body': json.dumps(items)
    }