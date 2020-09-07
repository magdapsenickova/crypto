
TEMPLATE = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
TEMPLATE_LENGTH = len(TEMPLATE)

# This is a single rotot implementation.
# Holds it's wiring and current position
class Rotor:

  # This is object constructor, takes following parameters:
  # - key: the rotor encryption key, required
  # - position: initial rotor position, required
  # - notchPosition: a rotor might have a notch, vhen reached, the next rotor is rotated
  def __init__(self, key: str, position: int = 0, notchPosition: int = None):
    assert len(key) == TEMPLATE_LENGTH, "illegal key, must be exactly 26 characters"
    self.key = bytearray(key, 'ascii')
    assert position >= 0, "illegal position, must not be negative"
    assert position < TEMPLATE_LENGTH, "illegal position, must not exceed key length"
    self.position = position
    self.notchPosition = notchPosition

  # Encode given char according to current rotor position
  # Based on https://math.dartmouth.edu/~jvoight/Fa2012-295/EnigmaSimManual.pdf
  def encode(self, char):
    idx = TEMPLATE.index(char)
    assert idx >= 0, 'cannot encode: ' + chr(char)

    rotTemplate = self.__rotatedTemplate()
    rotChar = self.__transcode(rotTemplate[idx])
    outIdx = self.__findOutIdx(rotChar)

    # Enable to check inividual rotor encoding
    # print("ENC", self.key.decode(), '(' + str(self.position) + ')', chr(char), '->', chr(rotChar), '->', chr(TEMPLATE[outIdx]))
    return TEMPLATE[outIdx]

  # Decode given char according to current rotor position
  # Based on https://math.dartmouth.edu/~jvoight/Fa2012-295/EnigmaSimManual.pdf
  def decode(self, char):
    idx = TEMPLATE.index(char)
    assert idx >= 0, 'cannot decode: ' + chr(char)

    rotTemplate = self.__rotatedTemplate()
    rotChar = rotTemplate[idx]
    inIdx = self.__findInIdx(rotChar)

    # Enable to check inividual rotor decoding
    # print("DEC", self.key.decode(), '(' + str(self.position) + ')', chr(char), '->', chr(rotChar), '->', chr(TEMPLATE[inIdx]))
    return TEMPLATE[inIdx]

  # Returns True when the rotor reached the notch position
  def isTurnover(self):
    return self.position == self.notchPosition

  # Performs one revelation of a rotor
  def rotate(self):
    self.position = self.position + 1
    if (self.position == TEMPLATE_LENGTH):
      self.position = 0

  # Returns the rotor template rotated according to position
  def __rotatedTemplate(self):
    return TEMPLATE[self.position:] + TEMPLATE[0:self.position]

  # This is the actual rotor wiring, for encoding 
  def __transcode(self, char):
    idx = TEMPLATE.index(char)
    return self.key[idx]

  # Find mapping to output character (position), for encoding
  def __findOutIdx(self, char):
    return TEMPLATE.index(char) - self.position

  # Find mapping to input character (position), for decoding
  def __findInIdx(self, char):
    return self.key.index(char) - self.position
