from z3 import *


def gint(n):
    return int(str(n))


enc = b'\x02\x19\x01\x16Q\r\x07\nS\x02)\x1a1=EE2\x0e=G/D\nRY)\nV\x1bJ'
key = [[0 for i in range(5)] for j in range(3)]
for i in range(3):
    for j in range(5):
        key[i][j] = BitVec('key[%d][%d]' % (i, j), 8)
inp = [0] * len(enc)
for i in range(len(inp)):
    inp[i] = BitVec('inp[%d]' % i, 8)

s = Solver()
for i in range(len(enc)):
    s.add(inp[i] ^ key[0][i % 5] ^ key[1][i % 5] ^ key[2][i % 5] == enc[i])

const = 'tjctf'
for i in range(len(const)):
  s.add(inp[i] == ord(const[i]))

k = [b'vsbb\x07', b'\x01@@@\x10', b'\x01@@@ ']

for i in range(3):
    for j in range(5):
        s.add(key[i][j] == k[i][j])
s.check()
m = s.model()
for i in range(len(inp)):
    print(chr(gint(m[inp[i]])), end='')
print()
