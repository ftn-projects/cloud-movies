import boto3

def handler(event, context):
    user_pool_id = event['userPoolId']
    group_name = 'User'
    username = event['userName']

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
    
    return event