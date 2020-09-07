from Rotor import Rotor, TEMPLATE
from Reflector import Reflector

# This is main class representing the ciphering machine
# It can be initialized with one or more rotors, each rotor with it's own settings
class RotorCipher:

  # This is a constructor method, this gets called when a new Cipher is created. 
  # Individual rotors must be created individually
  def __init__(self, rotors, reflector: Reflector):
    assert len(rotors) > 0, "illegal number of rotors, need at least one"
    self.rotors = rotors
    self.reflector = reflector
    
  # This is both encoding and decoding method
  def encode(self, message):
    buffer = bytearray(message, 'ascii')

    for i in range(len(buffer)):  
      # print("Encoding", chr(buffer[i]))

      # Do rotations first
      self.rotors[0].rotate()
      for j in range(1, len(self.rotors)):
        if (self.rotors[j-1].isTurnover()):
          self.rotors[j].rotate()

      # This is forward translation
      for j in range(len(self.rotors)):
        buffer[i] = self.rotors[j].encode(buffer[i])

      # Reflecting
      buffer[i] = self.reflector.reflect(buffer[i])
        
      # And backward translation
      for j in range(len(self.rotors)-1, -1, -1):
        buffer[i] = self.rotors[j].decode(buffer[i])

    return buffer.decode('ascii')
