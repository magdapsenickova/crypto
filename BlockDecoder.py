from AESConstants import BLOCK_SIZE, BLOCK_ROW_SIZE, BLOCK_COLUMN_SIZE, INVSBOX, ROUNDS, ROWS, COLUMNS, MUL9, MUL11, MUL13, MUL14
from BlockKey import BlockKey

# This is block decoding logic, used by Block during decode method.
# Requires a BlockKey to be created separately 
class BlockDecoder:

  # This is a constructor method
  #  - if data are not exactly BLOCK_SIZE long, an exception is raised
  def __init__(self, key: BlockKey, data: bytes):
    length = len(data)
    if (length != BLOCK_SIZE):
      raise Exception('illegal block size, must be exactly', BLOCK_SIZE, 'bytes')
    self.key = key
    self.data = data

  # This is decoding method, returns decoded data
  def decode(self):

    # Initial round
    finalKey = self.key.getRoundKey(ROUNDS)
    self.__addRoundKey(finalKey)
    self.__invShiftRows()
    self.__invSubBytes()

    # Main rounds
    for i in range(ROUNDS-1, 0, -1):

      # Generate the round key
      roundKey = self.key.getRoundKey(i)

      # Enable to see rounds in the console
      # print("> ROUND", i, "KEY", roundKey.hex())
      self.__addRoundKey(roundKey)
      self.__invMixColumns()
      self.__invShiftRows()
      self.__invSubBytes()

    # Final round
    self.__addRoundKey(self.key.getRoundKey(0))

    return self.data

  # Compute exclusive OR (https://en.wikipedia.org/wiki/Exclusive_or)
  # Validate using http://xor.pw
  def __addRoundKey(self, key: bytes):
    buffer = bytearray(self.data)
    for i in range(len(key)):
      # Enable to verify XORing
      # print('XOR(' + hex(self.data[i]) + ', ' + hex(key[i]) + ') =', hex(self.data[i] ^ key[i]))
      buffer[i] = self.data[i] ^ key[i]
    # Enable to verify the key munching
    # print("KEY", self.data.hex(), "->", buffer.hex())
    self.data = buffer

  # Unshift rows (rotate right)
  def __invShiftRows(self):
    buffer = bytearray(self.data)
    for i in range(0, ROWS):
      # get some data from the buffer into a row
      row = self.__getRow(i, buffer)
      # do the magic (rotate them)
      row = self.__invRotate(row, i)
      # and return back to buffer
      self.__updateRow(i, row, buffer)
    # Enable to verify the entire block shifting
    # print("ROW", self.data.hex(), "->", buffer.hex())
    self.data = buffer

  # Get one row of data
  # Please note: data are organized vertically, ie: bytes 00 01 02 ... 0F will be formed into the following matrix:
  # 00 04 08 0C
  # 01 05 09 0D
  # 02 06 0A 0E
  # 03 07 0B 0F
  # so first row will consist of bytes 00 04 08 0C
  # Strange, but defined like that in the specification.
  def __getRow(self, rowIdx, buffer):
    row = bytearray(BLOCK_ROW_SIZE)
    for j in range(0, BLOCK_ROW_SIZE):
      row[j] = buffer[(j * BLOCK_ROW_SIZE) + rowIdx]
    return row

  # Shift the buffer by given numberOfPositions to the right
  # Overflow bytes are rotated (e.g. last byte goes first)
  def __invRotate(self, buffer, numberOfPositions):
    idx = BLOCK_ROW_SIZE - numberOfPositions
    return buffer[idx:] + buffer[0:idx]

  # Update the buffer with given row of data
  # Please refer to __getRow method for row organization in the buffer
  def __updateRow(self, rowIdx, row, buffer):
    for j in range(0, BLOCK_ROW_SIZE):
      buffer[(j * BLOCK_ROW_SIZE) + rowIdx] = row[j]

  # Un-substitute bytes (substitute with inverse matrix)
  def __invSubBytes(self):
    buffer = bytearray(self.data)
    for i in range(BLOCK_SIZE):
      # Enable to verify SBOX lookup
      # print('INVSBOX(' + hex(self.data[i]) + ') =', hex(INVSBOX[self.data[i]]))
      buffer[i] = INVSBOX[self.data[i]]
    # Enable to verify the byte substitution
    # print("SUB", self.data.hex(), "->", buffer.hex())
    self.data = buffer

  # Unmix columns
  def __invMixColumns(self):
    buffer = bytearray(self.data)
    for i in range(0, COLUMNS):
      # get some data from the buffer
      column = self.__getColumn(i, buffer)
      # do the magic (rotate them)
      column = self.__invMix(column)
      # and return back to buffer
      self.__updateColumn(i, column, buffer)
    # Enable to verify the column munching
    # print("COL", self.data.hex(), "->", buffer.hex())
    self.data = buffer

  # Get given column of a buffer
  def __getColumn(self, colIdx, buffer):
    start = colIdx * BLOCK_COLUMN_SIZE
    end = start + BLOCK_COLUMN_SIZE
    return buffer[start:end]

  # Do the Gaulois mambo jumbo
  def __invMix(self, column):
    return [
      self.__gm(column[0], 14) ^ self.__gm(column[1], 11) ^ self.__gm(column[2], 13) ^ self.__gm(column[3], 9),
      self.__gm(column[0], 9)  ^ self.__gm(column[1], 14) ^ self.__gm(column[2], 11) ^ self.__gm(column[3], 13),
      self.__gm(column[0], 13) ^ self.__gm(column[1], 9)  ^ self.__gm(column[2], 14) ^ self.__gm(column[3], 11),
      self.__gm(column[0], 11) ^ self.__gm(column[1], 13) ^ self.__gm(column[2], 9)  ^ self.__gm(column[3], 14)
    ]

  # There are pre-calculated values for galois multiplication by 9, 11, 13 and 14
  # We do simple lookup into these tables
  def __gm(self, value, operator):
    if (operator == 9):
      return MUL9[value]
    if (operator == 11):
      return MUL11[value]
    if (operator == 13):
      return MUL13[value]
    if (operator == 14):
      return MUL14[value]
    return value

  # Update given column of a buffer with given data
  def __updateColumn(self, colIdx, column, buffer):
    start = colIdx * BLOCK_COLUMN_SIZE
    for i in range(BLOCK_COLUMN_SIZE):
      buffer[start+i] = column[i]