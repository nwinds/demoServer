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

# from hashlib import sha256
# import binascii
# import hmac
# import base64




# tid = hmac.new(secret, message, digestmod=sha256).digest()
# hextid = hmac.new(secret, message, digestmod=sha256).hexdigest()

# print(hextid)

# signature = binascii.b2a_hex(base64.b64encode(hmac.new(secret, message, digestmod=sha256).digest()))
# print(signature)
