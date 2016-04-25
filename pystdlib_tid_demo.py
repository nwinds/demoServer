from hashlib import sha256
import binascii
import hmac
import base64

import urllib
cid = 'ClientId00000001'
nonce = binascii.a2b_hex('0101010101010101')
authKey = 'ClientAuthKey001ClientAuthKey001'

message = bytes(cid + nonce).encode('utf-8')
secret = bytes(authKey).encode('utf-8')

tid = hmac.new(secret, message, digestmod=sha256).digest()
hextid = hmac.new(secret, message, digestmod=sha256).hexdigest()
count = 0
print(count),
print(hextid),
print('hextid')

signature = binascii.b2a_hex(base64.b64encode(tid))
count = 1
print(count),
print(signature)

base64_sign = base64.b64encode(tid)
count = 2
print(count),
print(base64_sign)

another_sign = base64.b64encode(base64_sign)
count = 2.5
print(count),
print(another_sign),
print('another_sign')

parses = {'tid': another_sign }
count = 3
print(count),
print(urllib.urlencode(parses))


"""
In [5]: base64.b64encode('l5Q430Y/RESzjxdHo9fDKPbmc4ERTCAAjNCWUPl+PRQ=')
Out[5]: 'bDVRNDMwWS9SRVN6anhkSG85ZkRLUGJtYzRFUlRDQUFqTkNXVVBsK1BSUT0='

In [6]: base64.b64decode('l5Q430Y/RESzjxdHo9fDKPbmc4ERTCAAjNCWUPl+PRQ=')
Out[6]: '\x97\x948\xdfF?DD\xb3\x8f\x17G\xa3\xd7\xc3(\xf6\xe6s\x81\x11L \x00\x8c\xd0\x96P\xf9~=\x14'

In [7]: binascii.hexlify(base64.b64decode('l5Q430Y/RESzjxdHo9fDKPbmc4ERTCAAjNCWUPl+PRQ='))
Out[7]: '979438df463f4444b38f1747a3d7c328f6e67381114c20008cd09650f97e3d14'

odd
"""
