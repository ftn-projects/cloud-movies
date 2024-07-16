import datetime
import json
import os
import boto3


dynamodb = boto3.resource('dynamodb')


def handler(event, context):
    table_name = os.getenv('VIDEOS_TABLE')
    table = dynamodb.Table(table_name)
    
    attributes = event['body']

    item = {}
    for param in ['title', 'description', 'releaseDate', 'genres', 'actors', 'directors']:
        item[param] = attributes[param]
    item['modified_at'] = datetime.now().isoformat()

    try:
        table.put_item(Item=item)
        status_code = 200
        body = item
    except Exception as e:
        print(e)
        status_code = 422
        body = {'error': 'Unable to save show details'}

    return { 
        'statusCode': status_code, 
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(body, default=str)
    }
