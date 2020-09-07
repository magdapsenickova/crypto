# This is a test

from AESCipher import AESCipher
from Crypto.Cipher import AES

# AES Cipher
# Test inspired by https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197.pdf

key = b'\x2b\x7e\x15\x16\x28\xae\xd2\xa6\xab\xf7\x15\x88\x09\xcf\x4f\x3c'
message = b'\x32\x43\xf6\xa8\x88\x5a\x30\x8d\x31\x31\x98\xa2\xe0\x37\x07\x34'
expresult = b'\x39\x25\x84\x1d\x02\xdc\x09\xfb\xdc\x11\x85\x97\x19\x6a\x0b\x32'
aesc = AESCipher(key)
aesc2 = AES.new(key, 1)

assert aesc.encrypt(message) == expresult  
assert aesc2.encrypt(message) == expresult
assert aesc.decrypt(expresult) == message
assert aesc2.decrypt(expresult) == message

print("AESCipher OK")

