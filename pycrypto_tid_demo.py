from Crypto.Hash import SHA256
from Crypto.Hash import HMAC
from binascii import b2a_hex
from binascii import a2b_hex
import base64

def hmac(key, data):
    if len(key) > 32:
        print("Warning")
    return HMAC.new(key, data, digestmod=SHA256).digest()

cid = 'ClientId00000001'
nonce = a2b_hex('0101010101010101')
authKey = 'ClientAuthKey001ClientAuthKey001'

message = bytes(cid + nonce).encode('utf-8')
secret = bytes(authKey).encode('utf-8')


print b2a_hex(base64.b64encode(hmac(secret, message)))

