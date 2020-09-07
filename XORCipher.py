from Cipher import Cipher

# This is main class representing the XOR cipher
class XORCipher(Cipher):

  # This is encoding method
  # It takes raw data input and produces encrypted data
  def encrypt(self, data: bytes):
    buffer = bytearray(len(data))
    for i in range(len(data)):
      idx = i % len(self.key)
      # Enable to verify XORing
      # print('XOR(' + hex(data[i]) + ', ' + hex(self.key[idx]) + ') =', idx, hex(data[i] ^ self.key[idx]))
      buffer[i] = data[i] ^ self.key[idx]
    return buffer

  # This is decoding method
  # In this case, to decrypt the data, just reapply the cipher
  def decrypt(self, data: bytes):
    return self.encrypt(data)
