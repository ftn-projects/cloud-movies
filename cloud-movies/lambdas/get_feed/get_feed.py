import boto3
import os
import json


dynamodb = boto3.resource('dynamodb')


def handler(event, context):
    table_name = os.getenv('FEEDS_TABLE')
    table = dynamodb.Table(table_name)

    userId = event['pathParameters']['userId']


    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('userId').eq(userId)
    )

    items = response['Items']

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(items, default=str)
    }
