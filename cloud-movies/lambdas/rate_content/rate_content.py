import os
import boto3
import json
import utils

def handler(event, context):
    table_name = os.getenv('RATINGS_TABLE')

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    user_id = event['pathParameters']['user_id']
    body = json.loads(event['body'])
    rating = int(body['rating'])
    content_id = body['contentId']

    if rating > 2 or rating < 0:
        return utils.create_response(400, 'Error: range must be in interval 0-2')

    if content_id is None:
        return utils.create_response(400, 'Error: content id is missing')

    # Should be checked if it exists?
    item = {
        'userId': user_id,
        'contentId': content_id,
        'rating': rating
    }

    try: 
        response = table.put_item(Item=item)
        return {
            'statusCode': 200,
            'body': json.dumps('Successfully rated'),
            'headers': {
                'Access-Control-Allow-Origin': '*',
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "POST,GET,OPTIONS",
            }
        }
    except Exception as e:
        return utils.create_response(400, f'Error inserting item {str(e)}')