from Crypto.Hash import HMAC
import Crypto
import binascii
cid = 'ClientId00000001'

authKey = b'ClientAuthKey001ClientAuthKey001'
# cid = 'ClientId00000001'
nonce = binascii.unhexlify('0101010101010101')

packed = cid+nonce
packed = b'%s' % packed
hmac = HMAC.new(authKey, 'Crypto.Hash.SHA256')
# hmac.update(cid)
hmac.update(nonce)
print(hmac.hexdigest())

