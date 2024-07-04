import os



def handler(event, context):
    source_bucket = os.environ['SOURCE_BUCKET']
    publish_bucket = os.environ['PUBLISH_BUCKET']

    resolution = event['resolution']
    object_key = event['objectKey']
    timestamp = event['timestamp']

    key, extension = object_key.split('.')
    partition_key, sort_key = key.split('_')

    new_key = f'{partition_key}_{sort_key}_{timestamp}_{resolution}.mp4'

    if 'meow' in object_key:
        raise ValueError(object_key)

    return {
        'objectKey': object_key
    }
