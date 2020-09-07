from AESConstants import BLOCK_SIZE, ROUNDS, BLOCK_ROW_SIZE, SBOX, RCON

# This class represents am encryption key.
# It is initialized with a key value and provides unique key for every encryption round. 
class BlockKey:

  # This is a constructor method, this gets called when a new BlockKey is created. 
  # It takes the key and verifies it's length (raises exception if not 16 bytes exact)
  def __init__(self, key: bytes):
    length = len(key)
    if (length != BLOCK_SIZE):
      raise Exception('illegal block size, must be exactly', BLOCK_SIZE, 'bytes')
    self.__expandedKey = self.__expandKey(key)

  # Generate the round key
  def getRoundKey(self, round: int):
    assert round <= ROUNDS, 'only ' + str(ROUNDS) + ' are available'
    start = BLOCK_SIZE * round
    end = start + BLOCK_SIZE 
    return self.__expandedKey[start:end]

  # Expands the key into an 176 bytes key
  def __expandKey(self, key: bytes):
    expKeySize = BLOCK_SIZE * (ROUNDS+1)
    expandedKey = bytearray(key)
    ckiteration = 1
    for i in range(len(key), expKeySize, BLOCK_ROW_SIZE):
      temp = expandedKey[i-BLOCK_ROW_SIZE:i]
      if (i % BLOCK_SIZE == 0):
        temp = self.__calculateKey(temp, ckiteration)
        ckiteration = ckiteration + 1
      for j in range(BLOCK_ROW_SIZE):
        idx = i - BLOCK_SIZE + j
        expandedKey.append(expandedKey[idx] ^ temp[j])
    # Enable to see the expanded key
    # print("EXP", key.hex(), "->", expandedKey.hex())
    return expandedKey
      
  # Calculate the expansion of one iteration, produced value
  # is appended to expandedKey
  def __calculateKey(self, part: bytes, iteration: int):
    part = self.__rotate(part, 1)
    for i in range(BLOCK_ROW_SIZE):
      part[i] = SBOX[part[i]]
    part[0] = part[0] ^ RCON[iteration]
    return part

  # Shift the buffer by given numberOfPositions to the left
  # Overflow bytes are rotated (e.g. first byte goes to the end)
  def __rotate(self, buffer, numberOfPositions):
    return buffer[numberOfPositions:] + buffer[0:numberOfPositions]
