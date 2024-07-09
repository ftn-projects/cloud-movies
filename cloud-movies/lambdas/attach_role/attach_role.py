import boto3
import json


def handler(event, context):
    group_name = 'User'

    message_str = event['Records'][0]['Sns']['Message']
    message_json = json.loads(json.loads(message_str)['default'])
    username = message_json['userName']
    user_pool_id = message_json['userPoolId']

    cognito_client = boto3.client('cognito-idp')    
    try:
        response = cognito_client.admin_add_user_to_group(
            UserPoolId=user_pool_id,
            Username=username,
            GroupName=group_name
        )
        print(f"User {username} added to group {group_name}")
    except Exception as e:
        print(f"Error adding user {username} to group {group_name}: {e}")
    
    return message_json
