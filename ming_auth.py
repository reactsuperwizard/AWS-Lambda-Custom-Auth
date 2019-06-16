import urllib.request
import json
import time
from jose import jwk, jwt
from jose.utils import base64url_decode

region = 'us-east-1'
userpool_id = 'us-east-1_70RGq0dzd'
app_client_id = '3ijq6ag7hihdm2rchduerhd0p4'
keys_url = 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format(region, userpool_id)
# instead of re-downloading the public keys every time
# we download them only on cold start
# https://aws.amazon.com/blogs/compute/container-reuse-in-lambda/
response = urllib.request.urlopen(keys_url)
keys = json.loads(response.read())['keys']



def generatePolicy(principalId, effect, methodArn):
    authResponse = {}
    authResponse['principalId'] = principalId
 
    if effect and methodArn:
        policyDocument = {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Sid': 'FirstStatement',
                    'Action': 'execute-api:Invoke',
                    'Effect': effect,
                    'Resource': methodArn
                }
            ]
        }
 
        authResponse['policyDocument'] = policyDocument
 
    return authResponse


'''
    token = id_token
    paramter = user_role

'''

def lambda_handler(event, context):    
    try :        
        
        token = event['authorizationToken']
        methodArn = event['methodArn']
        
        # get the kid from the headers prior to verification
        headers = jwt.get_unverified_headers(token)
        kid = headers['kid']
        
        # search for the kid in the downloaded public keys
        key_index = -1
        for i in range(len(keys)):
            if kid == keys[i]['kid']:
                key_index = i
                break
        
        if key_index == -1:
            return generatePolicy(None, 'Deny', methodArn)

        # construct the public key
        public_key = jwk.construct(keys[key_index])
        
        # get the last two sections of the token,
        # message and signature (encoded in base64)
        message, encoded_signature = str(token).rsplit('.', 1)
        
        # decode the signature
        decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))
        # verify the signature
        if not public_key.verify(message.encode("utf8"), decoded_signature):
            print('Signature verification failed')
            return generatePolicy(None, 'Deny', methodArn)
        
        
        print('Signature successfully verified')
        # since we passed the verification, we can now safely
        # use the unverified claims
        claims = jwt.get_unverified_claims(token)
        # additionally we can verify the token expiration
        
        if time.time() > claims['exp']:
            print('Token is expired')
            return generatePolicy(None, 'Deny', methodArn)
        
        # and the Audience  (use claims['client_id'] if verifying an access token)
        if claims['aud'] != app_client_id:
            print('Token was not issued for this audience')
            return generatePolicy(None, 'Deny', methodArn)
        
        # now we can use the claims
        principalId = claims['sub']
        
        return generatePolicy(principalId, 'Allow', methodArn)
    
    
    except Exception as ex:
        return generatePolicy(None, 'Deny', None)
        

if __name__ == '__main__':    
    # for testing locally you can enter the JWT ID Token here
    event = {
        "authorizationToken": "eyJraWQiOiJUcVd2NGlJQTR5NEsrMCtWSVRYMklYM2JDV1RVU3JoNnhNdGl5aVh5QkE0PSIsImFsZyI6IlJTMjU2In0.eyJjdXN0b206cmVnaW9uIjoidXMtZWFzdC0xIiwiYXRfaGFzaCI6InBkVVg4YmxiUVdCbmFmeFRiMzhkQ3ciLCJzdWIiOiJmYzdkNzJjNy01MGIzLTQ0NmEtYTE0NC03OTZhMDAxYzI3NjUiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLnVzLWVhc3QtMS5hbWF6b25hd3MuY29tXC91cy1lYXN0LTFfNzBSR3EwZHpkIiwicGhvbmVfbnVtYmVyX3ZlcmlmaWVkIjp0cnVlLCJjdXN0b206YWNjb3VudGlkIjoiMTkyODkxMDI5ODExIiwiY29nbml0bzp1c2VybmFtZSI6ImZjN2Q3MmM3LTUwYjMtNDQ2YS1hMTQ0LTc5NmEwMDFjMjc2NSIsImN1c3RvbTpvcmdhbml6YXRpb25pZCI6Im9nMzI3MDYyNjY2MSIsImF1ZCI6IjNpanE2YWc3aGloZG0ycmNoZHVlcmhkMHA0IiwidG9rZW5fdXNlIjoiaWQiLCJjdXN0b206Y2FtcHVzaWQiOiJjcDk2MTQ0MTQ4ODkiLCJhdXRoX3RpbWUiOjE1NjAxMzM0ODcsInBob25lX251bWJlciI6IisxOTU0ODYxNzI3MSIsImV4cCI6MTU2MDEzNzA4NywiY3VzdG9tOnJvbGUiOiJtYXN0ZXIiLCJpYXQiOjE1NjAxMzM0ODcsImN1c3RvbTplbnZpcm9ubWVudCI6ImRldiIsImVtYWlsIjoibGFzdGh5dW44MjJAZ21haWwuY29tIn0.L0s4f5vi7wdJ5HfyjAJ2e1aULLtf6QtyvVLH4J9cVHcZElwcvvWvrdKDukGb-qFVbduyBoC6uYrFGjxWwk7L7F9hSv8pgBBERgMQfz49_jBmbtotg88meFlcHsOLgFPv30r1x21FrLpLNz_K8GLBFUCK812qWVQLrdJLDQfP7sYr46Px5C1EC-2pdX-_KJXL7rpytf9yAdWPBj6_NOm43o7QL59pzzAQVb5VcGGgIlv1cRJcKCPfBQjwkyyN5GG8qw1DXFaRVTPTHjiirFRuiQ43Cd1GBJNWzATdNxBBQGZIzV_ZQYQlfDW4WJUkYTJLMjOyMddw-jZGbfM97rjyqA",
        "type": "TOKEN",
        "methodArn": "arn:aws:execute-api:us-east-1:848149494964:fw5uy6xu38/ESTestInvoke-stage/GET/"
    }    
    lambda_handler(event, None)