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