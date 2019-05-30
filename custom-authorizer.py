import json
import os
import logging
import jwt

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 
def get_json_from_jwt_token(jwt_token, secret_key, algorithms):
    
    return json.dumps(jwt.decode(jwt_token, secret_key))

# check jwt token with user role
def check_jwt_token(jwt_token, secret_key, algorithms):
    user_info_json = get_json_from_jwt_token(jwt_token, secret_key, algorithms)    
    
    return True


def custom_authorizer(event, context):

    try:

        logger.info(os.environ)
        logger.info(event)
        jwt_token = ''
        secret_key = ''
        algorithms=['HS256']

        if check_jwt_token(jwt_token, secret_key, algorithms):
            return {
                'statusCode': 200,
                'body': json.dumps('Hello from Lambda!')
            }
        else:
            return {
                'statusCode': 403,
                'body': json.dumps('Hello from Lambda!')
            }
    except Exception as ex:
        return {
            'statusCode': 500,
            'body': json.dumps('Interal Server Error!')
        }
