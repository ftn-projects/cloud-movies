import os
import boto3
import json
import utils
from urllib.parse import unquote_plus

def handler(event, context):
    table_name = os.getenv('SUBSCRIPTIONS_TABLE')

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    user_id = event['pathParameters']['userId']
    sub_type = event['pathParameters']['type']
    name = unquote_plus(event['pathParameters']['name']).strip()
    
    if name is None:
        return utils.create_response(400, 'Missing argument: name')

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
    try:
        response = table.delete_item(Key={'userId': user_id, 'subscriptionType': sk},
                                     ConditionExpression='attribute_exists(subscriptionType)'
                                     )

        return utils.create_response(200, 'Successfully unsubscribed')
    except Exception as e:
        return utils.create_response(400, f'Error: {str(e)}')