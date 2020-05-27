# Bad Python
> My friend wrote a cool program to encode text data! His code is sometimes hard to understand, and only he knows how it works. I ran the program twice, but forgot the input I used for the first time. I didn't save the key I used either, but I know it was 15 characters long. Can you figure out what text I encoded the first time?

The source code they give had been uglified. After some renaming, we get a new file:
```python
import random
import itertools
import functools

P = lambda a, b: (ord(a) ^ ord(b)).to_bytes(1, 'big')
E = ((0, 3), (1, 4), (0, 1), (3, 4), (2, 3), (1, 2))
B = sorted(list('ABCDEFGHIJKLMNO')) # -------------------------> 15 bytes key long
x = lambda a, b: ord(a) >= ord(b)
def u(li):
	Q = [li[i::3] for i in range(3)]
	for i in Q:
		while not W(i):
			pass
	return Q
def W(i):
	random.shuffle(i)
	a = [True]
	return [n(a, x(i[E[j][0]], i[E[j][1]])) for j in range(len(E))][-1]
def n(g, k):
	g[0] = g[0] and k
	return g[0]
f = u(B)

# print (f) # [['M', 'J', 'G', 'D', 'A'], ['N', 'K', 'H', 'E', 'B'], ['O', 'L', 'I', 'F', 'C']]


inp = open('input.txt', 'r').read()
m = 'output.txt'
open(m, 'w').write(
	repr(
		b''.join(
			[functools.reduce(P, [((ord(inp[i]) ^ ord(f[j][i % 5])).to_bytes(1, "big")) for j in range(len(f))]) for i in range(len(inp))])))
```
## Solution
We need to recover 15-byte key from `input2.txt` and `output2.txt`, then use this key and `output1.txt` to get the flag.
Run `key.py` to get the key, then feed this key to `flag.py` and get the flag
Flag: `tjctf{th15_iS_r3Al_pY7h0n_y4y}`.