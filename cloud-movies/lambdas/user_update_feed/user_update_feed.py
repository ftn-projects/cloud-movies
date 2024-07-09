import boto3
import json
import os


dynamodb = boto3.resource('dynamodb')


def handler(event, context):
    videos_table = os.environ['VIDEOS_TABLE']
    feeds_table = os.environ['FEEDS_TABLE']

    print(event)
