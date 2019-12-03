
from Crypto.Cipher import ARC4
from misc import tohex

def encrypt(s, key):
    r = ARC4.new(key).encrypt(s)
    return tohex(r).upper()
