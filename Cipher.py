
# This is generic class holding an encryption key.
class Cipher:

  # This is a constructor method, this gets called when a new Cipher is created. 
  # It takes the encoding key byte array as a parameter 'key'.
  def __init__(self, key: bytes):
    assert len(key) > 0, "no key given"
    self.key = key

  # This is encoding method
  # It takes raw data input and produces encrypted data, here it does nothing
  # Implementation is done in respective subclasses, such as AESCipher
  def encrypt(self, data: bytes):
    return data  

  # This is decoding method
  # It takes encrypted data input and produces original raw data, here it does nothing
  # Implementation is done in respective subclasses, such as AESCipher
  def decrypt(self, data: bytes):
    return data  
