# seed spring
> LongChampion, 06/04/2020

## Challenge
Guessing challenge!  
Just use `rand()` to generate 30 number with seed `time(0)` and send it to the server.
I have given the source and a compile binary to "predict" numbers.

## Solution
```python
#!/usr/bin/env python2
from pwn import *

r = remote("jh2i.com", 50010)
A = process(["./predict"]).recvall()
A = A[:-1].split('\n')
for x in A[:-1]:
    r.sendlineafter("height:", str(x))
    if "WRONG!" in r.recvline():
        print "WRONG!"
        break
print "Enter", A[-1], "to get the flag!"
r.interactive()
```
