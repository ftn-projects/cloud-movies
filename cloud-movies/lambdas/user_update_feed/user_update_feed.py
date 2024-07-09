import json
import boto3
import os
from boto3.dynamodb.conditions import Attr


dynamodb = boto3.client('dynamodb')
table = dynamodb.Table(os.getenv('FEEDS_TABLE'))
videos_table = dynamodb.Table(os.getenv('VIDEOS_TABLE'))

SUBSCRIPTION_DELTA = 10
RATING_DELTA = 3

contents = {}
for type in ['MOVIE', 'SHOW']:
    response = videos_table.scan(FilterExpression=Attr('videoType').eq(type))
    for item in response['Items']:
        contents[item['videoId']] = item


def add_subscription(user_id, subscription):
    response = table.get_item(Key={'userId': user_id})
    item = response['Item']

    for content in item['feed']:
        content = contents[content['contentId']]
        type, value = subscription.lower().split('::')

        if type == 'actor' and value in content['actors'].lower():
            content['rating'] += SUBSCRIPTION_DELTA
        elif type == 'director' and value in content['directors'].lower():
            content['rating'] += SUBSCRIPTION_DELTA
        elif type == 'genre' and value in content['genres'].lower():
            content['rating'] += SUBSCRIPTION_DELTA
    
    table.put_item(Item=item)


def add_rating(user_id, content_id, new_rating, old_rating=None):
    response = table.get_item(Key={'userId': user_id})
    item = response['Item']

    for content in item['feed']:
        if content['contentId'] == content_id:
            content['rating'] += new_rating - (0 if not old_rating else old_rating)
            break
    
    table.put_item(Item=item)


def remove_subscription(user_id, subscription):
    response = table.get_item(Key={'userId': user_id})
    item = response['Item']

    for content in item['feed']:
        content = contents[content['contentId']]
        type, value = subscription.lower().split('::')

        if type == 'actor' and value in content['actors'].lower():
            content['rating'] -= SUBSCRIPTION_DELTA
        elif type == 'director' and value in content['directors'].lower():
            content['rating'] -= SUBSCRIPTION_DELTA
        elif type == 'genre' and value in content['genres'].lower():
            content['rating'] -= SUBSCRIPTION_DELTA
    
    table.put_item(Item=item)


def remove_rating(user_id, content_id, rating):
    response = table.get_item(Key={'userId': user_id})
    item = response['Item']

    for content in item['feed']:
        if content['contentId'] == content_id:
            content['rating'] -= rating
            break
    
    table.put_item(Item=item)


def lambda_handler(event, context):
    record = event['Records'][0]
    body = json.loads(record['body'])
    dynamodb_event = body['dynamodb']
    event_name = body['eventName']

    if event_name == 'INSERT':
        new_image = dynamodb_event['NewImage']
        user_id = new_image['userId']['S']
        
        if 'subscriptionType' in new_image:
            add_subscription(user_id, new_image['subscriptionType']['S'])
        elif 'contentId' in new_image:
            add_rating(user_id, new_image['contentId']['S'], (int(new_image['rating']['S'])-1) * RATING_DELTA)

    if event_name == 'MODIFY':
        old_image = dynamodb_event['OldImage']
        new_image = dynamodb_event['NewImage']
        user_id = new_image['userId']['S']
        
        if 'contentId' in new_image:
            add_rating(user_id, new_image['contentId']['S'], (int(new_image['rating']['S'])-1) * RATING_DELTA, (int(old_image['rating']['S'])-1) * RATING_DELTA)

    if event_name == 'REMOVE':
        old_image = dynamodb_event['OldImage']
        user_id = old_image['userId']['S']
        
        if 'subscriptionType' in old_image:
            remove_subscription(user_id, old_image['subscriptionType']['S'])
        elif 'contentId' in old_image:
            remove_rating(user_id, old_image['contentId']['S'], (int(old_image['rating']['S'])-1)*RATING_DELTA)

    return {
        'statusCode': 200,
        'body': json.dumps('Processed successfully')
    }
