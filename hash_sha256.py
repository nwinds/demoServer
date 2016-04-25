from hashlib import sha256  # my pycrypto doesn't have SHA
from Crypto.Hash import HMAC
from binascii import a2b_hex

from Crypto.Hash import SHA256
# helper to match HMAC signature
class Sha256:
    @staticmethod
    def new():
        return sha256()

    # see http://stackoverflow.com/questions/30343741/build-hmac-sha-512-from-pycrypto-and-hashlib for further info
    block_size = sha256().block_size
    digest_size = sha256().digest_size
def hmac(hexkey, hexdata):
    return HMAC.new(a2b_hex(hexkey), a2b_hex(hexdata), digestmod=SHA256).hexdigest()

print hmac("436c69656e74417574684b6579303031436c69656e74417574684b6579303031",
     "0101010101010101")
#bugs  remained

