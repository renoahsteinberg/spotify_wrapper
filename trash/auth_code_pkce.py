import base64
from hashlib import sha256


class Authentication:
    def __init__(self, client_id):
        pass

    # Code Verifier

    def _generate_random_string(self, size=128, chars=string.ascii_letters + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    # Code Challenge

    def _sha256(self, plain):
        encoded_data = plain.encode('utf-8')
        sha256_hash = sha256(plain).digest()
        return sha256_hash

    def _base64encode(input):
        encoded = base64.b64encode(input).decode('utf-8')
        return encoded.replace('=', '').replace('+', '-').replace('/', '_')

    def authenticate(self):
        code_verifier = self._generate_random_string(size=64)
        hashed = self._sha256(code_verifier)
        code_challenge = self._base64encode(hashed)

        # GET to /authorize
