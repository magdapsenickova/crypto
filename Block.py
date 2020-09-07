from BlockKey import BlockKey
from BlockEncoder import BlockEncoder
from BlockDecoder import BlockDecoder

# This is a block operations implementation class, it uses two separate objects
# to handle the encoding and decoding work: BlockEncoder and BlockDecoder
class Block:

  # This is a constructor method
  def __init__(self, key: bytes):
    self.key = BlockKey(key)

  # This is block encoding method, uses BlockEncoder to do the hard work
  def encode(self, data: bytes):
    encoder = BlockEncoder(self.key, data)
    return encoder.encode()

  # This is block decoding method, uses BlockDecoder to do the hard work
  def decode(self, data: bytes):
    decoder = BlockDecoder(self.key, data)
    return decoder.decode()

