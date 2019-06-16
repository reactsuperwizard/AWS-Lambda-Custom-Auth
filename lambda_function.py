import json
import os
import logging
import jwt
import time


#   api params  
#       - id_token:
#       - access_token:
#       - role:
def check_parameters(params):
    try :
        if not params.get('id_token') or not params.get('access_token') or not params.get('parameter'):
            return False        
        return True    
    except Exception as Ex:
        raise ValueError("Parameter is not Correct")

def jwt_decode_param(token):    
    res = jwt.decode(token, verify=False)
    return res

def check_tokens(id_token, access_token, scope):
    try :
        # print(id_token)    
        # print(access_token)
        # print(scope)
        id_token_iss = id_token['iss']
        access_token_iss = access_token['iss']
        
        # token check
        if id_token_iss != access_token_iss:
            return False        
        
        # time check
        auth_time = access_token['auth_time']        
        exp_time = access_token['exp']
        cur_time = int(time.time())

        ## For Test 
        
        # if auth_time > cur_time or exp_time < cur_time:
        #     raise jwt.ExpiredSignatureError
            
        # sample Data from id_token
        # custom:region': 'us-east-1',
        # custom:accountid': '192891029811',
        # custom:organizationid': 'og3270626661',
        # custom:campusid': 'cp9614414889',
        # custom:role': 'master',
        # custom:environment': 'dev',
        
        
        if id_token['custom:region'] != scope['custom:region'] :
            return False

        if id_token['custom:accountid'] != scope['custom:accountid'] :
            return False

        if id_token['custom:organizationid'] != scope['custom:organizationid'] :
            return False


        if id_token['custom:role'] != scope['custom:role'] :
            return False

        if not id_token['custom:campusid'] in scope['custom:campusid'].split(",") :
            return False
    except Exception as ex:
        raise ex
        return False

    return True    

def lambda_handler(event, context):
      
    try :
        if not check_parameters(event):
            return {
                'statusCode': 401,
                'body': json.dumps('Parameter is not Correct!')
            }
        
        '''
            id_token - JWT String
            access_token - JWT String
            parameter - json string
        ''' 
        id_token = jwt_decode_param(event.get('id_token'))
        access_token = jwt_decode_param(event.get('access_token'))                
        parameter = json.loads(event.get('parameter'))
        
        if not check_tokens( id_token, access_token, parameter):
            return {
                'statusCode': 401,
                'body': json.dumps('Error: scope error.')
            }   
        return {
            'statusCode': 200,
            'body': json.dumps('Hello from Lambda!')
        }
    except KeyError:        
        return {
            'statusCode': 401,
            'body': json.dumps('Error: key error.')
        }
    except jwt.ExpiredSignatureError:        
        return {
            'statusCode': 401,
            'body': json.dumps('Error: expired token.')
        }                
    except jwt.DecodeError:        
        return {
            'statusCode': 401,
            'body': json.dumps('Error: decode error.')
        }        
    except Exception as ex:
        raise ex
        return {
            'statusCode': 500,
            'body': json.dumps('Internal Server Error!')
        }


if __name__ == "__main__":
    class Event:
        def get(self, key):
            e = {
                "id_token": "eyJraWQiOiJUcVd2NGlJQTR5NEsrMCtWSVRYMklYM2JDV1RVU3JoNnhNdGl5aVh5QkE0PSIsImFsZyI6IlJTMjU2In0.eyJjdXN0b206cmVnaW9uIjoidXMtZWFzdC0xIiwiYXRfaGFzaCI6ImZWcUd5ZTBzdGhsOTYwUkE0MVp6OFEiLCJzdWIiOiJmYzdkNzJjNy01MGIzLTQ0NmEtYTE0NC03OTZhMDAxYzI3NjUiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLnVzLWVhc3QtMS5hbWF6b25hd3MuY29tXC91cy1lYXN0LTFfNzBSR3EwZHpkIiwicGhvbmVfbnVtYmVyX3ZlcmlmaWVkIjp0cnVlLCJjdXN0b206YWNjb3VudGlkIjoiMTkyODkxMDI5ODExIiwiY29nbml0bzp1c2VybmFtZSI6ImZjN2Q3MmM3LTUwYjMtNDQ2YS1hMTQ0LTc5NmEwMDFjMjc2NSIsImN1c3RvbTpvcmdhbml6YXRpb25pZCI6Im9nMzI3MDYyNjY2MSIsImF1ZCI6IjNpanE2YWc3aGloZG0ycmNoZHVlcmhkMHA0IiwiZXZlbnRfaWQiOiI3YTU1OTRiMy04MzFkLTExZTktYWVmNC1jNWQ4NWVhOGJiZmUiLCJ0b2tlbl91c2UiOiJpZCIsImN1c3RvbTpjYW1wdXNpZCI6ImNwOTYxNDQxNDg4OSIsImF1dGhfdGltZSI6MTU1OTI0OTgyNCwicGhvbmVfbnVtYmVyIjoiKzE5NTQ4NjE3MjcxIiwiZXhwIjoxNTU5MjUzNDI0LCJjdXN0b206cm9sZSI6Im1hc3RlciIsImlhdCI6MTU1OTI0OTgyNCwiY3VzdG9tOmVudmlyb25tZW50IjoiZGV2IiwiZW1haWwiOiJsYXN0aHl1bjgyMkBnbWFpbC5jb20ifQ.UkacwOwXMDOhumDHyVWDuv7HMudQPU5Hw8dqsqCfdsPmrThbHCpUUjfPWKGZjMhtd6qSJvwIUnPIeYo48KzbmX90MNqA4OhE9YOARUHdt4aDCIkwRf-299a_yZ6ZGTGmUEEub0kMc4ehV7_Zjmmb3i3RTPQ9YdYVFvfvFlIyCrYKoxpT9G7D5ODiLaV3NYNMbxhrkut5SCMcBEs6iO1T_E9QdZarf6DSMLk6ft-XdsHpaYm4FqUbBi-mj6QFPCkozP4VqPZve57Po6nuVQwhdxY3SpP9AJD1DxZcQMZqMniFsoLGWj65Ptc9S7O2n7Fl9HUf84kkkIdX3UOmTXbA-Q",
                "access_token": "eyJraWQiOiJjT3JQNEJNbXo3dlZYNyszOWpCOFk0bGZWU2o4TWVVYWp6WUxmck1RcU9nPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJmYzdkNzJjNy01MGIzLTQ0NmEtYTE0NC03OTZhMDAxYzI3NjUiLCJldmVudF9pZCI6Ijc4NTBiNWM2LTgzNDgtMTFlOS05NzYwLTYxMjY3OTA5NzM1MSIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4gb3BlbmlkIHByb2ZpbGUgZW1haWwiLCJhdXRoX3RpbWUiOjE1NTkyNjgyODksImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xXzcwUkdxMGR6ZCIsImV4cCI6MTU1OTI3MTg4OSwiaWF0IjoxNTU5MjY4Mjg5LCJ2ZXJzaW9uIjoyLCJqdGkiOiIwMjg5YmVmNy03MGNjLTRkOGItODVlZi1mNWU3NTkyODEyODYiLCJjbGllbnRfaWQiOiIzaWpxNmFnN2hpaGRtMnJjaGR1ZXJoZDBwNCIsInVzZXJuYW1lIjoiZmM3ZDcyYzctNTBiMy00NDZhLWExNDQtNzk2YTAwMWMyNzY1In0.HvzdijEj-iBDaxXOCdqUnvkfFIHVGHXpk1UNOJqu8fXAWkUz0jdVGbJLEFjIkhRrQ6l1zAWW6To9RAURu7pRcVUEcHp8yffav9nw91RSXIosezJk4XWYdbescT7DOXgOaJqVhEdktLMjMvvYePeLU9NgMvEXAXxtjWyGAQlo4MzOAdbDs1ATgDOuXYwuOGGxnMdKx6uFhMyJGwsE0SOW9zbnUWJgNh8oiDQZuzgTFdNT4A11QhdK6EK0vqqQR9VenBDSc0knGjpenREByOxo19kJPM80u01SGFyw1NCym0wnFv8cka8uPva7LZX-SqcgowMswQl7toZYaTEfeEDbEg",
                "parameter": '''{
                            "custom:region":"us-east-1",
                            "custom:accountid":"192891029811",
                            "custom:organizationid":"og3270626661",
                            "custom:campusid":"cp9614414889, cp9614414889",
                            "custom:role":"master"
                    }'''
            }
            return e[key]

    context = 'context'
    event = Event()    
    res = lambda_handler(event, context)
    print(res)
    
    

    




