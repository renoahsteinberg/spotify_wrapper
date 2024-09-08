from flask import Flask, request, redirect
from dotenv import load_dotenv
import authorization
import os

app = Flask(__name__)

@app.route('/callback')
def callback():
    code = request.args.get('code')

    if code:
        token_data = auth._request_access_and_refresh_token(code)
        return f'Access token: {token_data}'
    else:
        return 'Auth failed'


if __name__ == '__main__':
    load_dotenv()

    auth = auth_code.Authentication(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri='http://localhost:8888/callback',
        scope='user-read-private user-read-email' 
    )

    token_data = auth.authenticate()
    
    app.run(debug=True, port=8888)