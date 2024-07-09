import json
import os
import boto3
from boto3.dynamodb.conditions import Attr

sns = boto3.client('sns')

def send_emails(topics, title):
    for sub_type, name in topics.items():
        for n in name:
            sub_name = str(n).replace(' ','_')
            topic_name = f'{sub_type}-{sub_name}'
         
            response = sns.create_topic(Name=topic_name)
            topic_arn = response['TopicArn']
            message = generate_message(sub_type, name, title)
            sns.publish(
                TopicArn=topic_arn,
                Message=message,
                Subject='New Content Notification',
            )

def generate_message(sub_type: str, name: str, title: str) -> str:
    message = f'New content available! \n'
    if sub_type == 'SHOW':
        message += f'New episode of {title} is now available, check out now! \n'
    else:
        message += f'{title} is now available, check out now! \n'
    message += f'You recieved this message because you are subscribed to topic {sub_type.lower()} - {name} \n'

    return message     

def handler(event, context):
    info = json.loads(event['Records'][0]['Sns']['Message'])
    videoType = info['videoType']

    topics = {
        'ACTOR': info['actors'].split(','),
        'DIRECTOR': info['directors'].split(','),
        'GENRE': info['genres'].split(','),
    }
    
    if str(videoType).startswith('SHOW'):
        topics['SHOW'] = [info['title']]
    
    send_emails(topics, info['title'])

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps({}, default=str)
    }
