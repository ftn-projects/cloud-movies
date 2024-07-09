import json
import boto3
import os


sns = boto3.client('sns')


def handler(event, context):
    topic_arn = os.environ['REGISTER_CONFIRMATION_TOPIC_ARN']
    print(event)

    sns.publish(
        TopicArn=topic_arn,
        Message=json.dumps({'default': json.dumps(event)}),
        Subject='New user registration'
    )

    return event
