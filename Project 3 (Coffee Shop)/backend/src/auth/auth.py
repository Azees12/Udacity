import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from ..errors import *


AUTH0_DOMAIN = 'dev-7e6cm0pp.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'Coffee Stack Shop'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''

## Auth Header

'''
@TODO implement get_token_auth_header() method
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    return the token part of the header
'''
def get_token_auth_header():

   header = request.headers.get('Authorization', None)

   if not header:
        raise invalid_header({
            'message':'Authorization header not found',
        })

   header_split = header.split(' ')

   if header_split[0] != 'BEARER':
       raise invalid_header({
             'message':'Authorization  header must begin with "Bearer" '
       })

   if len(header_split) == 1:
       raise invalid_header({
           'message':'No token was found'
       })
   
   if len(header_split) > 2:
       raise invalid_header({
           'message':'Authorization header must be a bearer token'
       })
    
   token = header_split[1]
   return token


 

'''
@TODO implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is not in the payload permissions array
    return true otherwise
'''
def check_permissions(permission, payload):
   
    if 'permissions' not in payload:
        raise invalid_header({
            'message':'No permission parameter found within JWT'
        })

    if permission not in payload['permission']:
        raise invalid_permissions({
            'message':'Permission not granted'
        })
    
    return True

    

'''
@TODO implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload

    !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''
def verify_decode_jwt(token):
    url = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(url.read())
    unverified_header  = jwt.get_unverified_header(token)
    rsa_key = {} 
    if 'kid' not in unverified_header:
        raise invalid_header({
            'message': 'Authorization malformed'
        })

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms = ALGORITHMS,
                audience = API_AUDIENCE,
                issuer = 'https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise token_expired
        
        except jwt.JWTClaimsError:
            raise invalid_claims

        except Exception:
            raise invalid_header
            

'''
@TODO implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the requested permission
    return the decorator which passes the decoded payload to the decorated method
'''
def requires_auth(permission=''):

    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator