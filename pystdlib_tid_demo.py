from hashlib import sha256
import binascii
import hmac
import base64

cid = 'ClientId00000001'
nonce = binascii.a2b_hex('0101010101010101')
authKey = 'ClientAuthKey001ClientAuthKey001'

message = bytes(cid + nonce).encode('utf-8')
secret = bytes(authKey).encode('utf-8')

tid = hmac.new(secret, message, digestmod=sha256).digest()
hextid = hmac.new(secret, message, digestmod=sha256).hexdigest()

print(hextid)

signature = binascii.b2a_hex(base64.b64encode(hmac.new(secret, message, digestmod=sha256).digest()))
print(signature)
