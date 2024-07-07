import json
import os
import boto3
import utils
from boto3.dynamodb.conditions import Key


dynamodb = boto3.resource('dynamodb')
sub_types = {
    'shows': 'SHOW::',
    'actors': 'ACTOR::',
    'directors': 'DIRECTOR::',
    'genres': 'GENRE::'
}


def handler(event, context):
    
    table_name = os.getenv('SUBSCRIPTIONS_TABLE')
    table = dynamodb.Table(table_name)

    user_id = event['pathParameters']['userId']
    items = generate_response(table, user_id)
    print(items)

    return utils.create_response(200, items)


def generate_response(table, user_id):
    r = {
        'actors': [],
        'shows': [],
        'directors': [],
        'genres': []
    }
    
    for dict_key, sub_type in sub_types.items():
        response = table.query(
            KeyConditionExpression=Key('userId').eq(user_id) & Key('subscriptionType').begins_with(sub_type)
        )    

        items = response.get('Items', [])        

        for item in items:
            name = item['subscriptionType'].split('::')[1]
            r[dict_key].append(name)
    return r