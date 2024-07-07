import os
import boto3
import json
import utils

def handler(event, context):
    table_name = os.getenv('SUBSCRIPTIONS_TABLE')

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    user_id = event['pathParameters']['userId']
    print(event['body'])
    body = json.loads(event['body'])
    print(body)
    sub_type = body['type']
    name = body['name'].strip()
    
    if name is None or sub_type is None:
        return utils.create_response(400, 'Missing argument')

    if sub_type == 'actors':
        sk = f'ACTOR::{name}'
    elif sub_type == 'directors':
        sk = f'DIRECTOR::{name}'
    elif sub_type == 'shows':
        sk = f'SHOW::{name}'
    elif sub_type == 'genres':
        sk = f'GENRE::{name}'
    else:
        return utils.create_response(400, 'Invalid subscription type')

    # Should be checked if it exists?
    item = {
        'userId': user_id,
        'subscriptionType': sk
    }

    try: 
        response = table.put_item(Item=item)

        return {
            'statusCode': 200,
            'body': json.dumps('Successfully subscribed'),
            'headers': {
                'Access-Control-Allow-Origin': '*',
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "POST,GET,OPTIONS",
            }
        }
    except Exception as e:
        return utils.create_response(400, f'Error inserting item {str(e)}')