import json
import os
import boto3


def handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table_name = os.getenv('VIDEOS_TABLE')
    table = dynamodb.Table(table_name)
    
    text = event['pathParameters']['text']
    items = []

    # Query by title
    response = table.query(
        IndexName='titleIndex',
        KeyConditionExpression=boto3.dynamodb.conditions.Key('title').eq(text)
    )
    items.extend(response['Items'])
    print(items)

    # Query by genres
    response = table.query(
        IndexName='genresIndex',
        KeyConditionExpression=boto3.dynamodb.conditions.Key('genres').eq(text)
    )
    items.extend(response['Items'])
    print(items)

    # Query by actors
    response = table.query(
        IndexName='actorsIndex',
        KeyConditionExpression=boto3.dynamodb.conditions.Key('actors').eq(text)
    )
    items.extend(response['Items'])
    print(items)

    # Query by directors
    response = table.query(
        IndexName='directorsIndex',
        KeyConditionExpression=boto3.dynamodb.conditions.Key('directors').eq(text)
    )
    items.extend(response['Items'])
    print(items)
    
    return {
        'statusCode': 200,
        'body': json.dumps(items)
    }