import os
import json
import base64
import string
import random
import requests
import webbrowser

from hashlib import sha256
from dotenv import load_dotenv
from urllib.parse import urlencode


AUTH_ENDPOINT = 'https://accounts.spotify.com/authorize?'
TOKEN_URL = 'https://accounts.spotify.com/api/token?'
REDIRECT_URI = 'https://eofwp2ac5gmtxx.m.pipedream.net'


def _random_string_generator(size=12, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def _sha256(plain):
    encoded_data = plain.encode('utf-8')
    sha256_hash = sha256(plain).digest()
    return sha256_hash

def _base64encode(input):
    encoded = base64.b64encode(input).decode('utf-8')
    return encoded.relace('=', '').replace('+', '-').replace('/', '_')

def _create_query_params(response_type, client_id, scope, redirect_uri, state):
    query_params = {
        'response_type': response_type,
        'client_id': client_id,
        'scope': scope,
        'redirect_uri': redirect_uri,
        'state': state
    }
    return query_params

def _request():
    pass


class AuthorizationCode:
    def __init__(self, client_id, client_secret, redirect_uri, scope, show_dialog):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.show_dialog = "" # ! yet to be implemented
    
    def _req_auth(self):
        state = _random_string_generator(size=12)

        return AUTH_ENDPOINT + urlencode(_create_query_params(
            response_type='code',
            client_id=self.client_id,
            scope=self.scope,
            redirect_uri=self.redirect_uri,
            state=state
        ))

    def _req_access_and_refresh_token(self, code):
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri,
            'client_id': self.client_id,
            'client_secretet': self.client_secret
        }

        response = requests.post(TOKEN_URL, data=data)

        return response.json() # TODO: Error Handling

    def auth(self):
        """
        Authentication Process:

        request authorization and create "auth_url" with self._req_auth
        then open the webbrowser for auth_url, after opening the webbrowser
        handle the callback with Flask (http://localhost:8888/callback) f.e. or your own redirect_uri.
        The callback will be for Flask (request.args.get('code')) and then needs to go through
        self._req_acess_and_refresh_token. Which then either returns the Access token or Failed Authentication
        """

        auth_url = self._req_auth()
        webbrowser.open(auth_url)

        # TODO
        
class AuthorizationCodePKCE:
    def __init__(self):
        pass

class ClientCredentials:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def _auth_header(self):
        auth_header = base64.b64encode(f'{self.client_id}:{self.client_secret}'.encode('ascii'))
        return {'Authorization': f'Basic {auth_header.decode('ascii')}'}

    def auth(self):
        data = {'grant_type': 'client_credentials'}

        response = requests.post(TOKEN_URL, headers=self._auth_header(), data=data)

        return response.json()

class ImplicitGrant:
    def __init__(self, client_id, redirect_uri, scope, show_dialog):
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.show_dialog = "" # ! yet to be implemented
    
    def _req_auth(self):
        state = _random_string_generator(size=16)

        return AUTH_ENDPOINT + urlencode(_create_query_params(
            response_type='token',
            client_id=self.client_id,
            scope=self.scope,
            redirect_uri=self.redirect_uri,
            state=state
        ))
    
    def auth(self):
        auth_url = self._req_auth()
        webbrowser.open(auth_url)

        # TODO

    # ! 'response_type': 'token'

class RefreshToken:
    def __init__(self):
        pass

    # ! https://developer.spotify.com/documentation/web-api/tutorials/refreshing-tokens
    # ! I have to safe tokens first, before starting to refresh them


if __name__ == '__main__':
    load_dotenv()

    #auth = ImplicitGrant(
    #    client_id=os.getenv('CLIENT_ID'),
    #    redirect_uri=REDIRECT_URI,
    #    scope='user-read-private user-read-email',
    #    show_dialog=""
    #)
    #auth.auth()

    #auth = ClientCredentials(
    #    client_id=os.getenv('CLIENT_ID'),
    #    client_secret=os.getenv('CLIENT_SECRET')
    #)
    #print(auth.auth())

    auth = AuthorizationCode(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri='https://127.0.0.1:8000/callback',
        scope='user-read-private user-read-email',
        show_dialog=""
    )
    token_data = auth.auth()