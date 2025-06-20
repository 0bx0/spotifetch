import base64
import hashlib
import os

def generate_pkce_pair():
    verif = base64.urlsafe_b64encode(os.urandom(64)).decode('utf-8').rstrip('=')
    chall = base64.urlsafe_b64encode(
        hashlib.sha256(verif.encode('utf-8')).digest()
    ).decode('utf-8').rstrip('=')
    return verif, chall
