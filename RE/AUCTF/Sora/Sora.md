# Sora
> xikhud, 05/04/2020.

## Problem
This is a simple challenge.

## Static analysis
This is the main function:
```cpp
int __cdecl main(int argc, const char **argv, const char **envp)
{
  __int64 v3; // rbp
  int result; // eax
  __int64 v5; // [rsp-38h] [rbp-38h]
  unsigned __int64 v6; // [rsp-10h] [rbp-10h]
  __int64 v7; // [rsp-8h] [rbp-8h]

  __asm { endbr64 }
  v7 = v3;
  v6 = __readfsqword(0x28u);
  sub_1110(stdout, 0LL, 2LL, 0LL);
  mb_puts("Give me a key!");
  mb_fgets(&v5, 30LL, stdin);
  if ( (unsigned int)encrypt((char *)&v5) )
  {
    print_flag();
    result = 0;
  }
  else
  {
    mb_puts("That's not it!");
    result = 1;
  }
  if ( __readfsqword(0x28u) != v6 )
    result = stack_chk();
  return result;
}
```
and the `encrypt` function:
```cpp
__int64 __fastcall encrypt(char *a1)
{
  int i; // [rsp-20h] [rbp-20h]

  __asm { endbr64 }
  for ( i = 0; i < (unsigned __int64)mb_strlen(secret); ++i )
  {
    if ( (8 * a1[i] + 19) % 61 + 65 != secret[i] )
      return 0LL;
      // secret = "aQLpavpKQcCVpfcg"
  }
  return 1LL;
}
```
# Solution
I simply bruteforce the flag using python.
```python
secret = 'aQLpavpKQcCVpfcg'

def brute():
	ret = ''
	for i in range(len(secret)):
		for j in range(256):
			if (8 * j + 19) % 61 + 65 == ord(secret[i]):
				ret += chr(j)
				break
	return ret

if __name__ == '__main__':
	print brute()
```
Using the script above, we got: `75<"72"%5($."0(`
And then:
```
(env) osboxes@osboxes:~/Desktop$ nc challenges.auctf.com 30004
Give me a key!
75<"72"%5($."0(
auctf{that_w@s_2_ezy_29302}
```
The flag is: `auctf{that_w@s_2_ezy_29302}`