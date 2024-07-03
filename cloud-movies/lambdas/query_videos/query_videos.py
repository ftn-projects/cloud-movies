import json
import os
import boto3
from boto3.dynamodb.conditions import Attr


def handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    
    table_name = os.getenv('VIDEOS_TABLE')
    table = dynamodb.Table(table_name)
    
    body = event['queryStringParameters']
    filters = {}

    if 'title' in body:
        filters['title'] = body['title']
    if 'description' in body:
        filters['description'] = body['description']
    if 'actors' in body:
        filters['actors'] = body['actors']
    if 'directors' in body:
        filters['directors'] = body['directors']
    if 'genres' in body:
        filters['genres'] = body['genres']

    filter_expression = None
    for key, value in filters.items():
        if filter_expression:
            filter_expression &= Attr(key).eq(value)
        else:
            filter_expression = Attr(key).eq(value)
    
    response = table.scan(FilterExpression=filter_expression)
    
    items = response.get('Items', [])
    
    while 'LastEvaluatedKey' in response:
        response = table.scan(
            FilterExpression=filter_expression,
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        items.extend(response.get('Items', []))
    
    return {
        'statusCode': 200,
        'body': json.dumps(items)
    }