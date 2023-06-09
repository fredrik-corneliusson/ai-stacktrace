import logging

import requests
from fastapi import HTTPException
from jose import jwt

region = 'eu-north-1'
userPoolId = 'eu-north-1_5614uLBuF'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def decode_token(token):
    key = get_public_key(token)
    try:
        payload = jwt.decode(token, key, algorithms=['RS256'])
    except jwt.JWTError as e:
        logger.info(f"JWT token error: {e}")
        raise HTTPException(status_code=403, detail="Invalid token")
    return payload


def get_public_key(token):
    header = jwt.get_unverified_header(token)
    jwks_url = f"https://cognito-idp.{region}.amazonaws.com/{userPoolId}/.well-known/jwks.json"
    jwks = requests.get(jwks_url).json()
    rsa_key = [k for k in jwks['keys'] if k['kid'] == header['kid']][0]
    return rsa_key
