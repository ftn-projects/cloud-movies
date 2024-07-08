import json
import os
import boto3


dynamodb = boto3.resource('dynamodb')


def handler(event, context):
    table_name = os.getenv('VIDEOS_TABLE')
    table = dynamodb.Table(table_name)
    
    show_id = json.loads(event['pathParameters']['showId'])
    season = json.loads(event['pathParameters']['season'])
    episode = json.loads(event['pathParameters']['episode'])
    
    key = {'videoId': show_id, 'videoType': f'SHOW::S{season:02d}::E{episode:02d}'}
    table_response = table.get_item(Key=key)
    
    if 'Item' not in table_response:
        status_code = 404
        body = {'error': 'Item not found'}
    else:
        status_code = 200
        body = {
            'title': table_response['Item']['title'],
            'description': table_response['Item']['description'],
            'releaseDate': table_response['Item']['releaseDate'],
        }
    
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(body, default=str)
    }
