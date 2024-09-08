"""
200 - OK - response header
201 - Created - new resource created
202 - Accepted - request accepted for processing
204 - No Content - succeeded but no return
304 - Not Modified - Cached version is still good
400 - Bad Request - Request could not be understood
401 - Unathorized - User requires authentication
403 - Forbidden - refusing to fullfil request
404 - Not Found
429 - Too Many Requests - Rate limiting applied
500 - Internal Server Error
502 - Bad Gateway - Server acting as a gateway or proxy received an invalid response from upstream server
503 - Service Unavailable - Server is currently unable to handle the request


Either Authentication Error Object or Regular Error Object
"""

import json
from time import sleep
from random import randint
from functools import wraps


def exponential_backoff(base, exp):
    return (base*2**exp) + (randint(0, 1000) / 1000)

def auto_retry(backoff_in_seconds=1, retries=3, retry_codes=[404]):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retry = 0
            while True:
                if retry == retries:
                    raise Exception("too many retries")

                response = func(*args, **kwargs)

                if response.status_code == 200:
                    return json.loads(response.content)
                elif response.status_code in retryCodes:
                    delay = exponential_backoff(backoff_in_seconds, retry)
                    sleep(delay)
                else:
                    raise Exception(response.status_code)

                retry += 1
            return wrapper
        return decorator