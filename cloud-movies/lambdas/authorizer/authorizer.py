import os
import json
import jwt.algorithms
import jwt.types
import requests
from jwt import PyJWKClient
import jwt 


REGION = os.getenv('REGION')
USER_POOL_ID = os.getenv('USER_POOL_ID')
CONGITO_CLIENT_ID = os.getenv('COGNITO_CLIENT_ID')

ROLE_ACCESS_CONTROL = {
    'Admin': ['GET/admin', 'GET/user'],
    'User': ['GET/user', 'GET/upload']
}

def get_jwks():
    jwks_url = f'https://cognito-idp.{REGION}.amazonaws.com/{USER_POOL_ID}/.well-known/jwks.json'
    response = requests.get(jwks_url)
    response.raise_for_status()
    return response.json()

def decode_jwt(token, jwks):
    try:
        decoded_header = jwt.get_unverified_header(token)
        decoded_token = jwt.decode(token, options={'verify_signature': False})
        
        user_pool_keys = jwks['keys']
        kid = decoded_header['kid']
        
        use_keys = [key for key in user_pool_keys if key['kid']==kid]
        if len(use_keys) != 1:
            raise ValueError('Error obtaining the keys')
        print(use_keys) 
        try:
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(use_keys[0])
            decoded_token = jwt.decode(token, public_key, algorithms=['RS256'])
            return decoded_token
        except Exception as e:
            print(str(e))
            raise ValueError('Error validating token')

    except Exception as e:
        print(str(e))
        raise ValueError('oops')

def generate_policy(principal_id, effect, method_arn):
    return {
        'principalId': principal_id,
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Action': 'execute-api:Invoke',
                    'Effect': effect,
                    'Resource': method_arn
                }
            ]
        }
    }

def check_authorization(roles, method_arn):
    method, path = method_arn.split('/')[2:4]
    print(method, path)
    for role in roles:
        if role in ROLE_ACCESS_CONTROL:
            print('aaaa')
            for access_pattern in ROLE_ACCESS_CONTROL[role]:
                access_method, access_path = access_pattern.split('/', 1)
                print(access_method, access_path)
                if method == access_method and (path == access_path or access_path == '*'):
                    print('Yipi')
                    return True
    return False

def handler(event, context):
    print(event)
    token = event['authorizationToken'].split(' ')[1]
    method_arn = event['methodArn']
    jwks = get_jwks()
    try:
        print('123123', jwks)
        decode_token = decode_jwt(token, jwks)
        roles = decode_token.get('cognito:groups', [])
        user_id = decode_token['sub']
        print(roles, user_id)

        if check_authorization(roles=roles, method_arn=method_arn):
            return generate_policy(user_id, 'Allow', method_arn)
        else:
            return generate_policy(user_id, 'Deny', method_arn)
        
    except jwt.ExpiredSignatureError as e:
        print(str(e))
        return generate_policy('user', 'Deny', method_arn)
    except jwt.InvalidTokenError as e:
        print(str(e))
        return generate_policy('user', 'Deny', method_arn)
    except Exception as e:
        print(str(e))
        return generate_policy('user', 'Deny', method_arn)