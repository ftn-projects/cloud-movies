import json
import decimal

class CustomJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super().default(o)

def create_response(status, body):
    return { 
        'statusCode': status, 
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(body, default=str)
        }
