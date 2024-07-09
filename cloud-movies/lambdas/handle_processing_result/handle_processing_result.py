import boto3
import json
import os


s3_client = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')


def handler(event, context):
    publish_bucket = os.environ['PUBLISH_BUCKET']
    source_bucket = os.environ['SOURCE_BUCKET']
    videos_table = os.environ['VIDEOS_TABLE']
    resolutions = os.environ['RESOLUTIONS'].split(',')
    published_video_arn = os.environ['PUBLISHED_VIDEO_ARN']

    info = json.loads(event['Records'][0]['Sns']['Message'])
    if info['state'] == 'unzipping': return


    if info['success'] == True: object_key = info['objectKey']
    else: object_key = json.loads(info['error'])['errorMessage']
    primary_key, sort_key, timestamp, extension = object_key.split('_')
    source_key = f'{primary_key}_{sort_key}.{extension}'
    publish_key = f'{primary_key}_{sort_key}_{timestamp}'

    objects = {}
    for res in resolutions:
        objects[res] = s3_client.Object(publish_bucket, f'{publish_key}_{res}.mp4')


    if info['success'] == True:
        table = dynamodb.Table(videos_table)
        table.update_item(
            Key={'videoId': primary_key, 'videoType': sort_key},
            UpdateExpression='SET files = :val',
            ExpressionAttributeValues={':val': {
                res: {'path': f'{publish_key}_{res}.mp4', 'size': obj.content_length} for res, obj in objects.items()
            }}
        )
        response = table.get_item(
            Key={'videoId': primary_key, 'videoType': sort_key}
        )

        sns.publish(
            TopicArn=published_video_arn,
            Subject='Video published',
            Message=json.dumps(response['Item'])
        )

    else:
        table = dynamodb.Table(videos_table)
        table.delete_item(Key={'videoId': primary_key, 'videoType': sort_key})
        for obj in objects.values(): obj.delete()

    s3_client.Object(source_bucket, source_key).delete()
