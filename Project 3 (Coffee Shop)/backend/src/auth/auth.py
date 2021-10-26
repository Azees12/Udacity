import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from ..errors import *


AUTH0_DOMAIN = 'dev-7e6cm0pp.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'Coffee Stack Shop'

## Auth Header
def get_token_auth_header():

   header = request.headers.get('Authorization', None)

   if not header:
        raise invalid_header({
            'status': 'auth_header_notfound',
            'message':'Authorization header not found'
        })

   header_split = header.split(' ')

   if header_split[0].lower() != 'bearer':
       raise invalid_header({
             'status': 'invalid_header',
             'message':'Authorization  header must begin with "Bearer" '
       })

   if len(header_split) == 1:
       raise invalid_header({
           'status': 'invalid_header',
           'message':'No token was found'
       })
   
   if len(header_split) > 2:
       raise invalid_header({
           'status': 'invalid_header',
           'message':'Authorization header must be a bearer token'
       })
    
   token = header_split[1]
   return token


def check_permissions(permission, payload):
    
    if 'permissions' not in payload:
        raise invalid_header({
            'status': 'no_permissions_found',
            'message':'No permission parameter found within JWT'
        })

    if permission not in payload['permissions']:
        raise invalid_permissions({
            'status': 'permission_invalid',
            'message':'Permission not granted'
        })
    
    return True

    
def verify_decode_jwt(token):
    url = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(url.read())
    unverified_header  = jwt.get_unverified_header(token)
    rsa_key = {} 
    if 'kid' not in unverified_header:
        raise invalid_header({
            'status': 'invalid_header',
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
            raise token_expired()
        
        except jwt.JWTClaimsError:
            raise invalid_claims()

        except Exception:
            raise invalid_header()
            
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