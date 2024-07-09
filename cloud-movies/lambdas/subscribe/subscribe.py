import os
import boto3
import json
import utils

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

def subscribe_to_sns(email: str, subscription_type: str):
    topic_name = subscription_type.replace('::','-').replace(' ', '_')
    response = sns.create_topic(Name=topic_name)
    topic_arn = response['TopicArn']
    print(topic_arn)
    sns.subscribe(
        TopicArn=topic_arn,
        Protocol='email',
        Endpoint=email
    )

def handler(event, context):

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
        email = get_user_email(user_id)
        if email == '':
            return utils.create_response(400, 'Error')
        subscribe_to_sns(email, sk)

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
    

