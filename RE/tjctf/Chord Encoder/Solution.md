# Chord encoder
We have a `python` file:
```python
f = open('song.txt').read()

l = {'1':'A', '2':'B', '3':'C', '4':'D', '5':'E', '6':'F', '7':'G'}
chords = {}
for i in open('chords.txt').readlines():
	c, n = i.strip().split()
	chords[c] = n

s = ''
for i in f:
	c1, c2 = hex(ord(i))[2:]
	if c1 in l:
		c1 = l[c1]
	if c2 in l:
		c2 = l[c2]
	s += chords[c1] + chords[c2]
open('notes.txt', 'w').write(s)
```
`chords.txt`
```
A 0112
B 2110
C 1012
D 020
E 0200
F 1121
G 001
a 0122
b 2100
c 1002
d 010
e 0100
f 1011
g 000
```
`notes.txt`
```
1121112111211002112101121121001001210000101221121011200102000110120200101100100111211011001020020010111012011202001011112110121121011211211002112110020200101111210112020010111121010112102001121100211211011020020001010
```
## Solution
```python
from sys import exit
from binascii import *

chords = {
'A':  '0112',
'B':  '2110',
'C':  '1012',
'D':  '020',
'E':  '0200',
'F':  '1121',
'G':  '001',
'a':  '0122',
'b':  '2100',
'c':  '1002',
'd':  '010',
'e':  '0100',
'f':  '1011',
'g':  '000'
}

enc = '1121112111211002112101121121001001210000101221121011200102000110120200101100100111211011001020020010111012011202001011112110121121011211211002112110020200101111210112020010111121010112102001121100211211011020020001010'
length = len(enc)
l = {'1':'A', '2':'B', '3':'C', '4':'D', '5':'E', '6':'F', '7':'G'}

def brute(enc, res, cur):
	if cur >= length:
		print ('[+] ' + res)
		return
	tmp = enc[cur:cur + 4]
	for k in chords:
		if chords[k] == tmp:
			brute(enc, res + k, cur + 4)
	tmp = enc[cur:cur + 3]
	for k in chords:
		if chords[k] == tmp:
			brute(enc, res + k, cur + 3)

def main():
	# brute(enc, '', 0)
	s = 'FFFcFAFGGbGaFAGDGCEfGGFfGDEfCAEfFCFAFcFcEfFAEfFdFEFcFfDDGd'
	r = ''
	for char in s:
		is_in = False
		for k in l:
			if l[k] == char:
				r += k
				is_in = True
		if not is_in:
			r += char
	print (a2b_hex(r).decode())
	return 0

if __name__ == '__main__':
	exit(main())
```
flag: `flag{zats_wot_1_call_a_meloD}`