"""
header = {'Authorization':'Bearer ' + access_token}
"""

from dotenv import load_dotenv
import os


# importing secrets
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


