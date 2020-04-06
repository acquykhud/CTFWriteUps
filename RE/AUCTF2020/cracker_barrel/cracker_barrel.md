# Cracker Barrel
> xikhud, 05/04/2020.

## Problem
The binary is simple, just connect to server, input password 3 times, and it will give us the flag if the password is correct.
```cpp
mb_fgets(&v2, 0x2000LL, stdin);
remove_newline(&v2);
if ( check_1((__int64)&v2)
    && (mb_puts("You have passed the first test! Now I need another key!"),
        mb_fgets(&v2, 0x2000LL, stdin),
        remove_newline(&v2),
        check_2((__int64)&v2))
    && (mb_puts("Nice work! You've passes the second test, we aren't done yet!"),
        mb_fgets(&v2, 0x2000LL, stdin),
        remove_newline(&v2),
        (unsigned int)check_3((char *)&v2)) )
  {
    mb_puts("Congrats you finished! Here is your flag!");
    result = 1LL;
  }
```
## Static analysis
3 check routines:
```cpp
bool check_1(__int64 a1)
{
  bool result; // rax
  if ( (unsigned int)mb_strcmp(a1, "starwars") )
    result = 0LL;
  else
    result = (unsigned int)mb_strcmp(a1, "startrek") != 0;
  return result;
}

bool check_2(__int64 a1)
{
  int i; // [rsp-20h] [rbp-20h]
  int v3; // [rsp-1Ch] [rbp-1Ch]
  char *v4; // [rsp-10h] [rbp-10h]

  v3 = mb_strlen(a1);
  v4 = (char *)mb_malloc(8LL * (v3 + 1));
  for ( i = 0; i < v3; ++i )
  {
    v4[i] = aSiSihtEgassemT[v3 - 1 - i];
    // aSiSihtEgassemT = "si siht egassem terces"
  }
  return (unsigned int)mb_strcmp(v4, a1) == 0;
}

__int64  check_3(char *a1)
{
  __int64 v1; // rax
  __int64 result; // rax
  int i; // [rsp-5Ch] [rbp-5Ch]
  int v4; // [rsp-58h] [rbp-58h]
  int j; // [rsp-54h] [rbp-54h]
  int *v6; // [rsp-50h] [rbp-50h]
  int v7; // [rsp-48h] [rbp-48h]
  int v8; // [rsp-44h] [rbp-44h]
  int v9; // [rsp-40h] [rbp-40h]
  int v10; // [rsp-3Ch] [rbp-3Ch]
  int v11; // [rsp-38h] [rbp-38h]
  int v12; // [rsp-34h] [rbp-34h]
  int v13; // [rsp-30h] [rbp-30h]
  int v14; // [rsp-2Ch] [rbp-2Ch]
  int v15; // [rsp-28h] [rbp-28h]
  int v16; // [rsp-24h] [rbp-24h]
  unsigned __int64 v17; // [rsp-20h] [rbp-20h]
  __int64 v18; // [rsp-8h] [rbp-8h]

  v17 = __readfsqword(0x28u);
  v7 = 'z';
  v8 = '!';
  v9 = '!';
  v10 = 'b';
  v11 = '6';
  v12 = '~';
  v13 = 'w';
  v14 = 'n';
  v15 = '&';
  v16 = '`';
  v1 = mb_strlen(a1);
  v6 = (int *)mb_malloc(4 * v1);
  for ( i = 0; i < (unsigned __int64)mb_strlen(a1); ++i )
    v6[i] = (a1[i] + 2) ^ 0x14;
    
  v4 = 0;
  for ( j = 0; j < (unsigned __int64)mb_strlen(a1); ++j )
  {
    if ( v6[j] != *((_DWORD *)&v18 + j - 16) )
      v4 = 1;
  }
  result = v4 == 0;
  if ( __readfsqword(0x28u) != v17 )
    result = stack_chk();
  return result;
}
```
We can easily see that, the first password is `starwars`, and the second password is `secret message this is`.
With the last password, it first get encrypted, and then compare to a hardcoded array, but it only compare `strlen(password)` bytes, which mean we can input the password with one byte length.
We must have: `v6[0]  =  (password[0]  +  2)  ^  0x14` and `v6[0] == 'z'`, so `password[0]` must be `'l'`.

# Solution
```
(env) osboxes@osboxes:~/Desktop$ nc challenges.auctf.com 30000
Give me a key!
starwars
You have passed the first test! Now I need another key!
secret message this is
Nice work! You've passes the second test, we aren't done yet!
l
Congrats you finished! Here is your flag!
auctf{w3lc0m3_to_R3_1021}
```
The flag is: `auctf{w3lc0m3_to_R3_1021}`.