
from XORCipher import XORCipher

# XOR cipher
# This cipher is initialized with a key, any length
# Test using https://www.dcode.fr/xor-cipher
# with ASCII key 'secret' and HEX output

xorc = XORCipher(b'secret')
assert xorc.encrypt(b'\x00\xff') == b'\x73\x9a'
assert xorc.encrypt(b'hello') == b'\x1b\x00\x0f\x1e\x0a'
assert xorc.encrypt(b'\x00\x00\x00\x00\x00\x00') == b'secret'
assert xorc.decrypt(b'\x1b\x00\x0f\x1e\x0a') == b'hello'
assert xorc.encrypt(b'hello world') == b'\x1b\x00\x0f\x1e\x0a\x54\x04\x0a\x11\x1e\x01'
assert xorc.decrypt(b'\x1b\x00\x0f\x1e\x0a\x54\x04\x0a\x11\x1e\x01') == b'hello world'
assert xorc.encrypt(b'') == b''
print("XORCipher OK")