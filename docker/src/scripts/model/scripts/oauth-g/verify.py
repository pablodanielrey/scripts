"""
https://developers.google.com/identity/sign-in/web/build-button
"""

from google.oauth2 import id_token
from google.auth.transport import requests

import logging
logging.getLogger().setLevel(logging.INFO)

import sys

# (Receive token by HTTPS POST)
# ...

try:
    token = sys.argv[1]
    logging.info('Tratando de verificar el token : {}'.format(token))

    CLIENT_ID = '777095490716-2e6oj15p7s2tqhou9rfe8gvvg7f4v9d2.apps.googleusercontent.com'
    idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

    logging.info(idinfo)

    # Or, if multiple clients access the backend server:
    # idinfo = id_token.verify_oauth2_token(token, requests.Request())
    # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
    #     raise ValueError('Could not verify audience.')

    if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
        raise ValueError('Wrong issuer.')

    # If auth request is from a G Suite domain:
    # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
    #     raise ValueError('Wrong hosted domain.')

    # ID token is valid. Get the user's Google Account ID from the decoded token.
    userid = idinfo['sub']

except ValueError as e:
    # Invalid token
    logging.exception(e)
