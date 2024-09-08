import os
import string
import random
import requests
import webbrowser
import json
from dotenv import load_dotenv
from urllib.parse import urlencode
# ! from my_dec.request_decorator import auto_retry

# TODO: Sometimes multiple spotify logins opening, also handle flask differently
# TODO: implement scope and dialog in future
# TODO: Read more into the acutal authentication process

# ? used in a mobile or web application, will implement further later


class Authentication:
    def __init__(self, client_id="", client_secret="", redirect_uri="", scope=""):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = scope
        
        #self.show_dialog = "" # ! not implemented till later versions

        self.auth_code = None

        self.END_POINT = 'https://accounts.spotify.com/authorize?'
        

    def _state_generator(self, size=12, chars=string.ascii_letters + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def _request_authorization(self):
        state = self._state_generator()

        query_params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'scope': self.scope,
            'redirect_uri': self.redirect_uri,
            'state': state
        }

        return self.END_POINT + urlencode(query_params)

    #@auto_retry()
    def _request_access_and_refresh_token(self, code):
        token_url = 'https://accounts.spotify.com/api/token?'

        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }

        response = requests.post(token_url, data=data)

        return response.json() # TODO: Implement error codes

    def authenticate(self):
        auth_url = self._request_authorization()

        print(f'Authorize on: {auth_url}')
        webbrowser.open(auth_url)

        code = input('Enter Authorization Code: ')

        if code:
            token = self._request_access_and_refresh_token(code)
            print(f'Access Granted: {code}')
        else:
            print('Access Denied')

    

