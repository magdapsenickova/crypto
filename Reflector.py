
TEMPLATE = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# This is a reflector implementation.
class Reflector:

  # This is object constructor, takes following parameters:
  # - key: the reflector encryption key
  def __init__(self, key: str):
    assert len(key) == len(TEMPLATE), "illegal key, must be exactly 26 characters"
    self.key = bytearray(key, 'ascii')

  # Encode given char
  def reflect(self, char):
    idx = TEMPLATE.index(char)
    assert idx >= 0, 'cannot encode: ' + chr(char)

    # Enable to check reflector encoding
    # print("REF", self.key.decode(), chr(char), '->', chr(self.key[idx]))
    return self.key[idx]

