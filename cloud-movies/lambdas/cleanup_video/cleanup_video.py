import boto3
import json
import os


s3_client = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')


def handler(event, context):
    source_bucket = os.environ['SOURCE_BUCKET']
    publish_bucket = os.environ['PUBLISH_BUCKET']
    videos_table = os.environ['VIDEOS_TABLE']

    print(event)

    info = json.loads(event['Records'][0]['Sns']['Message'])

    success = bool(info['success'])

    if not success and info['state'] == 'transcoding':
        print('errorMessage: ' + json.loads(info['error']))
        object_key = json.loads(info['error'])['errorMessage']
    else:
        object_key = info['objectKey']

    # cleanup all files

    # s3_client.Object(source_bucket, object_key).delete()
    # if not success:
    #     s3_client.Object(publish_bucket, object_key).delete()