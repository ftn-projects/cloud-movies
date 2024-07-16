import os
import boto3
import json
import utils
from urllib.parse import unquote_plus

table_name = os.getenv('SUBSCRIPTIONS_TABLE')
userpool_id = os.getenv('USERPOOL_ID')

sns = boto3.client('sns')
cognito = boto3.client('cognito-idp')
dynamodb = boto3.resource('dynamodb')

def get_user_email(sub: str):
    try:
        response = cognito.list_users(
            UserPoolId=userpool_id,
            Filter=f'sub = "{sub}"',
            AttributesToGet=['email']
        )
        print('aaaa', response)
        if 'Users' in response:
            user = response['Users'][0]
            email = user['Attributes'][0]['Value'] # since we are returning only email
            print(email) 
            return email

    except Exception as e:
        print('Error getting user email: {e}')
        return ''

def unsubscribe_from_sns(email: str, subscription_type: str):
    topic_name = subscription_type.replace('::','-').replace(' ', '_')
    
    response = sns.create_topic(Name=topic_name)
    topic_arn = response['TopicArn']
    
    response = sns.list_subscriptions_by_topic(
        TopicArn=topic_arn
    )
    
    if 'Subscriptions' in response:
        for subs in response['Subscriptions']:
            if subs['Endpoint'] == email:
                sns.unsubscribe(
                    SubscriptionArn=subs['SubscriptionArn']
                )
    

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
        email = get_user_email(user_id)
        unsubscribe_from_sns(email, sk)
        return utils.create_response(200, 'Successfully unsubscribed')
    except Exception as e:
        return utils.create_response(400, f'Error: {str(e)}')