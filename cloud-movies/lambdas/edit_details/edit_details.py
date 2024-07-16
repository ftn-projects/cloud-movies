import datetime
import json
import os
import boto3


def handler(event, context):
    dynamodb = boto3.resource('dynamodb')

    table_name = os.getenv('VIDEOS_TABLE')
    table = dynamodb.Table(table_name)
    
    video_id = json.loads(event['pathParameters']['videoId'])
    video_type = json.loads(event['pathParameters']['videoType'])
    value = event['body']

    key = {'videoId': video_id, 'videoType': video_type}
    response = table.get_item(Key=key)

    if 'Item' in response:
        item = response['Item']

        for param in ['title', 'description', 'releaseDate', 'genres', 'actors', 'directors']:
            item[param] = value[param]

        item['modified_at'] = datetime.now().isoformat()

        table.put_item(Item=item)
        status_code = 200
        body = item
    else:
        status_code = 404
        body = {'error': 'Item not found'}

    return { 
        'statusCode': status_code, 
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(body, default=str)
    }