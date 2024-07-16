import json
import boto3
import os


dynamodb = boto3.client('dynamodb')
table = dynamodb.Table(os.getenv('FEEDS_TABLE'))
videos_table = dynamodb.Table(os.getenv('VIDEOS_TABLE'))
subscriptions_table = dynamodb.Table(os.getenv('SUBSCRIPTIONS_TABLE'))
ratings_table = dynamodb.Table(os.getenv('RATINGS_TABLE'))

SUBSCRIPTION_DELTA = 10
RATING_DELTA = 3


def scan_table(table):
    items = []
    response = table.scan()
    items.extend(response.get('Items', []))
    
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        items.extend(response.get('Items', []))
    
    return items


def lambda_handler(event, context):
    record = event['Records'][0]
    body = json.loads(record['body'])
    sns_message = json.loads(body['Message'])
    video_id = sns_message.get['videoId']

    items = scan_table(table)

    for item in items:
        user_id = item['userId']
        feed = item['feed']

        feed.append({
            'contentId': video_id,
            'rating': 50
        })
        
        table.put_item(Item={
            'userId': user_id,
            'feed': feed
        })

    return {
        'statusCode': 200,
        'body': json.dumps('Processed successfully')
    }
