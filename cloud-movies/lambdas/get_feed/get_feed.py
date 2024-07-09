import boto3
import os
import json
from boto3.dynamodb.conditions import Key


dynamodb = boto3.resource('dynamodb')


def handler(event, context):
    videos_table = dynamodb.Table(os.getenv('VIDEOS_TABLE'))
    table_name = os.getenv('FEEDS_TABLE')
    table = dynamodb.Table(table_name)

    userId = event['pathParameters']['userId']


    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('userId').eq(userId)
    )

    s = sorted(response['Item']['feed'], key=lambda x: x['rating'], reverse=True)

    all_items = []
    for id in [item['contentId'] for item in s]:
        for content_type in ['SHOW', 'MOVIE']:
            response = videos_table.query(
                KeyConditionExpression=Key('videoId').eq(id) & Key('videoType').eq(content_type),
                ProjectionExpression='videoType,actors,videoId,title,directors,releaseDate,description,#time,genres',
                ExpressionAttributeNames={"#time": "duration"})
            items = response.get('Items', [])
            print(items) 
            all_items.extend(items)

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(items, default=str)
    }
