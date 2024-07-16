import os
import boto3
from boto3.dynamodb.conditions import Key
import utils

def handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    
    table_name = os.getenv('VIDEOS_TABLE')
    table = dynamodb.Table(table_name)
    all_items = []
    for content_type in ['SHOW', 'MOVIE']:
        response = table.query(
            IndexName='videoTypeIndex',
            KeyConditionExpression=Key('videoType').eq(content_type),
            ProjectionExpression='videoType,actors,videoId,title,directors,releaseDate,description,#time,genres',
            ExpressionAttributeNames={"#time": "duration"})
        items = response.get('Items', [])
        print(items) 
        all_items.extend(items)

    return utils.create_response(200, all_items)
