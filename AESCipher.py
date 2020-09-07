from AESConstants import BLOCK_SIZE
from Block import Block
from Cipher import Cipher

# This is main class representing the AES cipher
class AESCipher(Cipher):

  # This is main encoding method
  # It takes raw data input and produces encrypted data
  def encrypt(self, data: bytes):
    buffer = b''
    for i in range(0, len(data), BLOCK_SIZE):
      block = Block(self.key)
      buffer += block.encode(data[i:i+BLOCK_SIZE])
    return buffer  

  # This is main decoding method
  # It takes encrypted data input and produces original raw data
  def decrypt(self, data: bytes):
    buffer = b''
    for i in range(0, len(data), BLOCK_SIZE):
      block = Block(self.key)
      buffer += block.decode(data[i:i+BLOCK_SIZE])
    return buffer  
