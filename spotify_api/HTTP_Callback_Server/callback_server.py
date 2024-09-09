#!/usr/bin/env python

import os
import ssl
import http.server
import urllib.parse


class oAuth2CallbackHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)

        if 'code' in params:
            auth_code = params['code'][0]
            print(f'Received Auth Code: {auth_code}')
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<html><body><h1>Authorization code received. You can close this window.</h1></body></html>')
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<html><body><h1>No Authorization code received.</h1></body></html>')

script_dir = os.path.dirname(os.path.abspath(__file__))
cert_file = os.path.join(script_dir, "cert.pem")
key_file = os.path.join(script_dir, "key.pem")

server_adress = ('127.0.0.1', 8000)
httpd = http.server.HTTPServer(server_adress, oAuth2CallbackHandler)

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile=cert_file, keyfile=key_file)

httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

print("Starting HTTPS Server on https://127.0.0.1:8000")
httpd.serve_forever()