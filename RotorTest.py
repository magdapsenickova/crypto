from RotorCipher import RotorCipher
from Rotor import Rotor
from Reflector import Reflector

from pyenigma import rotor, enigma

# Rotor cipher
# This is initialized with a list of preconfigured rotors an a reflector
# Test using https://www.101computing.net/enigma-machine-emulator/ 
# with rotors I, II and III, rings A-A-A, initial position A-A-A

r1 = Rotor('BDFHJLCPRTXVZNYEIWGAKMUSQO') # fastest rotor, type III
r2 = Rotor('AJDKSIRUXBLHWTMCQGZNPYFVOE') # rotor type II
r3 = Rotor('EKMFLGDQVZNTOWYHXUSPAIBRCJ') # slowest rotor, type I
ref = Reflector('YRUHQSLDPXNGOKMIEBFZCWVJAT')
rotc = RotorCipher([r1, r2, r3], ref) 
assert rotc.encode('AAAAA') == 'BDZGO'
assert r1.position == 5
assert r2.position == 0
assert r3.position == 0

r1.position = 0
assert rotc.encode('BDZGO') == 'AAAAA'

# Notching
# Note the non-standard notch position for Rotor III, emulator will not produce the same result

r1 = Rotor('BDFHJLCPRTXVZNYEIWGAKMUSQO', 0, 1) # fastest rotor, notch at B
rotc = RotorCipher([r1, r2, r3], ref) 
assert rotc.encode('HELLO') == 'QKGWG'   
assert r1.position == 5
assert r2.position == 1
assert r3.position == 0

# Verify using pyenigma, https://pypi.org/project/pyenigma/

pye = enigma.Enigma(rotor.ROTOR_Reflector_B, rotor.ROTOR_III, rotor.ROTOR_II, rotor.ROTOR_I)
assert pye.encipher("AAAAA") == 'BDZGO' # This is famous text, try googling it
# Existing pye's rotors are now rotated, need to create new instance to reset 
pye = enigma.Enigma(rotor.ROTOR_Reflector_B, rotor.ROTOR_III, rotor.ROTOR_II, rotor.ROTOR_I)
assert pye.encipher("BDZGO") == 'AAAAA'

print("ROTCipher OK")

