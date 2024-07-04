from datetime import datetime
import logging
import zipfile
import boto3
import json
import uuid
import os


METADATA_EXTENSION = '.json'

s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')
sns_client = boto3.client('sns')
dynamodb = boto3.resource('dynamodb')

tmp_file_path = '/tmp/file.zip'


def handler(event, context):
    extensions = os.environ['EXTENSIONS'].split(',')
    videos_table = os.environ['VIDEOS_TABLE']
    failed_topic_arn = os.environ['FAILED_TOPIC_ARN']

    bucket = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']

    try:
        logging.info(f'Processing object {object_key} from bucket {bucket}')
        s3_resource.Object(bucket, object_key).download_file(tmp_file_path)

        with zipfile.ZipFile(tmp_file_path, 'r') as zip_ref:
            files = [f for f in zip_ref.namelist() if not f.startswith('__MACOSX')]
            video_files = [f for f in files if any(f.endswith(ext) for ext in extensions)]
            json_files = [f for f in files if f.endswith(METADATA_EXTENSION)]

            if len(files) != 2 or len(video_files) != 1 or len(json_files) != 1:
                raise ValueError('Zip file must contain exactly one video file and one metadata file.')

            logging.info(f'Processing video file {video_files[0]} and metadata file {json_files[0]}')
            metadata = process_metadata(zip_ref.read(json_files[0]))

            logging.info(f'Uploading video file {video_files[0]} and metadata to DynamoDB')
            dynamodb.Table(videos_table).put_item(Item=metadata)
            
            logging.info(f'Uploading video file {video_files[0]} to S3')
            s3_client.put_object(
                Bucket=bucket, 
                Key=get_new_key(video_files[0], metadata), 
                Body=zip_ref.read(video_files[0])
            )
    except ValueError as e:
        logging.error(f'Error processing object {object_key} from bucket {bucket}: {str(e)}')
        sns_client.publish(
            TopicArn=failed_topic_arn,
            Subject='Failed to process source bucket object',
            Message=json.dumps({
                'success': False,
                'state': 'unzipping',
                'objectKey': object_key
            })
        )
    finally:
        s3_resource.Object(bucket, object_key).delete()
        cleanup_tmp_files()


def process_metadata(text: bytes) -> dict:
    loaded_json = json.loads(text.decode('utf-8'))
    now = datetime.now().isoformat()

    metadata = {
        'title': loaded_json['title'].strip(),
        'description': loaded_json['description'].strip(),
        'releaseDate': datetime.strptime(loaded_json['releaseDate'], '%Y-%m-%d').isoformat(),
        'duration': int(loaded_json['duration']),
        'status': 'created',
        'created_at': now,
        'modified_at': now,
        'files': {'360': {}, '480': {}, '720': {}}
    }

    if loaded_json['type'].upper() == 'MOVIE':
        metadata.update({
            'videoId': str(uuid.uuid4()),
            'videoType': 'MOVIE',
            'genres': loaded_json['genres'],
            'actors': loaded_json['actors'],
            'directors': loaded_json['directors']
        })
    else:
        season, episode = int(loaded_json['season']), int(loaded_json['episode'])
        metadata.update({
            'videoId': loaded_json['showId'],
            'videoType': f'SHOW::S{season:02d}::E{episode:02d}',
            'season': season,
            'episode': episode
        })

    return metadata


def get_new_key(video_key: str, metadata: dict) -> str:
    extension = video_key.split('.')[-1]
    return f"{metadata['videoId']}_{metadata['videoType']}.{extension}"


def cleanup_tmp_files():
    if os.path.exists(tmp_file_path):
        os.remove(tmp_file_path)
    for file in os.listdir("/tmp"):
        os.remove(os.path.join("/tmp", file))
