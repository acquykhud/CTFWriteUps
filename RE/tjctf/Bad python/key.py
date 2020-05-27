from z3 import *

def gint(n):
  return int(str(n))

enc = b':\x1c\x10\x07ZV\x1a\x12\x11B\x1bS\x06\r[\x19\x01B\x11^\x02S\x03\x0fR\x02_B\x01X\x18\x00\x07\x01C\x13\x07\x17\x10\x17\x17\x17\x0b\x12^\x05\x10\x0b\x0cPV\x16\x0e\x0bC'
key = [[0 for i in range(5)] for j in range(3)]
for i in range(3):
  for j in range(5):
    key[i][j] = BitVec('key[%d][%d]' % (i,j), 8)
inp = [0] * len(enc)
for i in range(len(inp)):
  inp[i] = BitVec('inp[%d]' % i, 8)

s = Solver()
for i in range(len(enc)):
  s.add(inp[i] ^ key[0][i%5] ^ key[1][i%5] ^ key[2][i%5] == enc[i])
const = 'Lorem '
for i in range(len(const)):
  s.add(inp[i] == ord(const[i]))
for i in range(3):
  for j in range(5):
    s.add(key[i][j] != 0)
print (s.check())
m = s.model()
for i in range(len(inp)):
  print (chr(gint(m[inp[i]])), end = '')
print ()
for i in range(3):
  for j in range(5):
    print ((gint(m[key[i][j]])), end = ',')
print ()