import json
import os
import boto3
from boto3.dynamodb.conditions import Key

def handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    
    table_name = os.getenv('SUBSCRIPTIONS_TABLE')
    table = dynamodb.Table(table_name)

    user_id = json.loads(event['pathParameters']['user_id'])
    
    response = table.query(
        KeyConditionExpression=Key('user_id').eq(user_id)
    )
    
    items = response.get('Items', [])
    
    while 'LastEvaluatedKey' in response:
        response = table.query(
            KeyConditionExpression=Key('user_id').eq(user_id),
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        items.extend(response.get('Items', []))
    
    return {
        'statusCode': 200,
        'body': json.dumps(items)
    }