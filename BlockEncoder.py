from AESConstants import BLOCK_SIZE, BLOCK_ROW_SIZE, BLOCK_COLUMN_SIZE, SBOX, MUL2, MUL3, ROUNDS, ROWS, COLUMNS, FILLIN_CHAR
from BlockKey import BlockKey

class BlockEncoder:

  # This is a constructor method
  #  - if data are too short, there are some FILLIN characters added at the end
  #  - if data are too long, an exception is raised
  def __init__(self, key: BlockKey, data: bytes):
    length = len(data)
    if (length < BLOCK_SIZE):
      data = data + FILLIN_CHAR * (BLOCK_SIZE-length)
    elif (length > BLOCK_SIZE):
      raise Exception('illegal block size, must be exactly', BLOCK_SIZE, 'bytes')
    self.key = key
    self.data = data

  # This is encoding method, returns encoded data
  def encode(self):

    # Initial round
    self.__addRoundKey(self.key.getRoundKey(0))

    # Main rounds
    for i in range(1, ROUNDS):

      # Generate the round key
      roundKey = self.key.getRoundKey(i)

      # Enable to see rounds in the console
      # print("> ROUND", i, "KEY", roundKey.hex())
      self.__subBytes()
      self.__shiftRows()
      self.__mixColumns()
      self.__addRoundKey(roundKey)
		
    # Final round
    finalKey = self.key.getRoundKey(i+1)
    # Enable to see final round in the console
    # print("> FINAL KEY", roundKey.hex())
    self.__subBytes()
    self.__shiftRows()
    self.__addRoundKey(finalKey)

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

  # Substitute bytes, find a byte at index equal to input bte value
  # Please note the 0-based array, so value 8 will be found at index 9
  def __subBytes(self):
    buffer = bytearray(self.data)
    for i in range(BLOCK_SIZE):
      # Enable to verify SBOX lookup
      # print('SBOX(' + hex(self.data[i]) + ') =', hex(SBOX[self.data[i]]))
      buffer[i] = SBOX[self.data[i]]
    # Enable to verify the byte substitution
    # print("SUB", self.data.hex(), "->", buffer.hex())
    self.data = buffer

  # Shift rows as follows: row 0 not shifted, row 1 shifted by 1, row 2 shifted by 2 etc., all left
  def __shiftRows(self):
    buffer = bytearray(self.data)
    for i in range(0, ROWS):
      # get some data from the buffer into a row
      row = self.__getRow(i, buffer)
      # do the magic (rotate them)
      row = self.__rotate(row, i)
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

  # Shift the buffer by given numberOfPositions to the left
  # Overflow bytes are rotated (e.g. first byte goes to the end)
  def __rotate(self, buffer, numberOfPositions):
    return buffer[numberOfPositions:] + buffer[0:numberOfPositions]

  # Update the buffer with given row of data
  # Please refer to __getRow method for row organization in the buffer
  def __updateRow(self, rowIdx, row, buffer):
    for j in range(0, BLOCK_ROW_SIZE):
      buffer[(j * BLOCK_ROW_SIZE) + rowIdx] = row[j]

  # Mix columns using 
  def __mixColumns(self):
    buffer = bytearray(self.data)
    for i in range(0, COLUMNS):
      # get some data from the buffer
      column = self.__getColumn(i, buffer)
      # do the magic (rotate them)
      column = self.__mix(column)
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
  def __mix(self, column):
    return [
      self.__gm(column[0], 2) ^ self.__gm(column[1], 3) ^ self.__gm(column[2], 1) ^ self.__gm(column[3], 1),
      self.__gm(column[0], 1) ^ self.__gm(column[1], 2) ^ self.__gm(column[2], 3) ^ self.__gm(column[3], 1),
      self.__gm(column[0], 1) ^ self.__gm(column[1], 1) ^ self.__gm(column[2], 2) ^ self.__gm(column[3], 3),
      self.__gm(column[0], 3) ^ self.__gm(column[1], 1) ^ self.__gm(column[2], 1) ^ self.__gm(column[3], 2)
    ]

  # There are pre-calculated values for galois multiplication by 2 and 3
  # We do simple lookup into MUL2 and MUL3 tables
  def __gm(self, value, operator):
    if (operator == 2):
      return MUL2[value]
    if (operator == 3):
      return MUL3[value]
    return value

  # Update given column of a buffer with given data
  def __updateColumn(self, colIdx, column, buffer):
    start = colIdx * BLOCK_COLUMN_SIZE
    for i in range(BLOCK_COLUMN_SIZE):
      buffer[start+i] = column[i]