import json
import os
import boto3
from boto3.dynamodb.conditions import Key


dynamodb = boto3.resource('dynamodb')


def handler(event, context):
    table_name = os.getenv('VIDEOS_TABLE')
    table = dynamodb.Table(table_name)
    
    show_id = json.loads(event['pathParameters']['showId'])
    season = json.loads(event['pathParameters']['season'])
    episode = json.loads(event['pathParameters']['episode'])
    
    response = table.query(
        KeyConditionExpression=Key('videoId').eq(show_id) & Key('videoType').begins_with(f'SHOW::S{season:02d}')
    )

    seasons = [i for i in response['Items'] if 'E' not in i['videoType']][0]
    episodes = [i for i in response['Items'] if 'E' in i['videoType']]

    if len(seasons) < 0:
        status_code = 404
        body = {'error': 'Season not found'}
    else:
        status_code = 200
        season = seasons[0]
        body = {
            'title': season['title'],
            'releaseDate': season['releaseDate'],
            'episodes': [
            {
                'title': e['title'],
                'description': e['description'],
                'releaseDate': e['releaseDate']            
            } for e in episodes]
        }
    
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(body, default=str)
    }