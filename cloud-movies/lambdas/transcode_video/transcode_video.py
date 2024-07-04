import os
import boto3
import subprocess

FFMPEG_STATIC = "/opt/ffmpeg"
VIDEO_EXTENSIONS = ['mp4', 'mov', 'm4v']

def handler(event, context):
    source_bucket = os.environ['SOURCE_BUCKET']
    publish_bucket = os.environ['PUBLISH_BUCKET']

    resolution = event['resolution']
    object_key = event['objectKey']
    timestamp = event['timestamp']

    key, extension = object_key.split('.')
    partition_key, sort_key = key.split('_')

    new_key = f'{partition_key}_{sort_key}_{timestamp}_{resolution}.mp4'

    if extension not in VIDEO_EXTENSIONS:
        print(f'Cannot transcode {extension} files')
        raise Exception(f'{partition_key}_{sort_key}_{timestamp}_{extension}')

    try:
        if not os.path.isdir(f'/tmp/{resolution}'):
            os.mkdir(f'/tmp/{resolution}')
        download_file(source_bucket, object_key, resolution)
        ffmpeg_command = f'{FFMPEG_STATIC} -i "/tmp/{resolution}/{object_key}" -vf scale=-2:{resolution} "/tmp/{resolution}/{new_key}"'
        subprocess.run(ffmpeg_command, shell=True)
        print("MJAU MJAU MJAU MJAU MJAU")
        print(os.path.getsize(f'/tmp/{resolution}/{new_key}'))
        print(os.path.getsize(f'/tmp/{resolution}/{object_key}'))
        upload_file(publish_bucket, new_key, resolution)

    except Exception as e:
        print(f"Exception {str(e)}")
        raise Exception(f'{partition_key}_{sort_key}_{timestamp}_{extension}')

    finally:
        os.remove(f'/tmp/{resolution}/{object_key}')
        os.remove(f'/tmp/{resolution}/{new_key}')

    return {
        'objectKey': f'{partition_key}_{sort_key}_{timestamp}_{extension}'
    }


def download_file(bucket_name, key, resolution):
    s3 = boto3.resource('s3')
    s3.Bucket(bucket_name).download_file(key, f'/tmp/{resolution}/{key}')


def upload_file(bucket_name, key, resolution):
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(f'/tmp/{resolution}/{key}', bucket_name, key)

