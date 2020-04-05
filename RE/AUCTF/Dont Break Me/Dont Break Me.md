# Don't Break Me!
> xikhud, 05/04/2020.

## Problem
This is a simple challenge, but it has a debugger check routine, which make dynamic analysis harder !

## Static analysis
This is the main function:
```cpp
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char s; // [esp+0h] [ebp-2018h]
  char *s1; // [esp+2000h] [ebp-18h]
  char *s2; // [esp+2004h] [ebp-14h]
  int v7; // [esp+2008h] [ebp-10h]
  int v8; // [esp+200Ch] [ebp-Ch]
  int *v9; // [esp+2010h] [ebp-8h]

  v9 = &argc;
  setvbuf(stdout, 0, 2, 0);
  puts(
    "54 68 65 20 6d 61 6e 20 69 6e 20 62 6c 61 63 6b 20 66 6c 65 64 20 61 63 72 6f 73 73 20 74 68 65 20 64 65 73 65 72 74"
    " 2c 20 61 6e 64 20 74 68 65 20 67 75 6e 73 6c 69 6e 67 65 72 20 66 6f 6c 6c 6f 77 65 64 2e");
  debugger_check();
  v8 = 17;
  v7 = 12;
  printf("Input: ");
  fgets(&s, 0x2000, stdin);
  remove_newline(&s);
  s2 = encrypt(&s, v8, v7);
  s1 = (char *)calloc(0x20u, 4u);
  get_string(s1);
  if ( !strcmp(s1, s2) )
    print_flag();
  else
    printf("Not quite");
  return 0;
}
```
This is the `debugger_check` function:
```
.text:00001219                 push    ebp
.text:0000121A                 mov     ebp, esp
.text:0000121C                 call    __x86_get_pc_thunk_ax
.text:00001221                 add     eax, 2DDFh
.text:00001226                 mov     ecx, 400h
.text:0000122B                 mov     eax, 0CCh
.text:00001230
.text:00001230 loc_1230:                               ; DATA XREF: debugger_check:antiBpLoop↓r
.text:00001230                 call    $+5
.text:00001235                 pop     edi
.text:00001236                 sub     edi, 5
.text:00001239
.text:00001239 antiBpLoop:                             ; CODE XREF: debugger_check+26↓j
.text:00001239                 cmp     byte ptr ds:(loc_1230 - 1230h)[edi], al
.text:0000123B                 jz      short DebuggerDetected
.text:0000123D                 inc     edi
.text:0000123E                 dec     ecx
.text:0000123F                 jnz     short antiBpLoop
.text:00001241                 nop
.text:00001242                 pop     ebp
.text:00001243                 retn
```
Note: when we set a breakpoint in `gdb` using `b *address` command, it will patch the byte at address to `0xCC`, which is `int 3` instruction.
This function check `0x400` bytes from offset `0x1235` to find a byte with value `0xCC`, if found, that means the process is being attached by a debugger.
# Solution
In the `main` function, we see that, the program wait for us to input a password, then the password is encrypted and then compare to a hardcoded one.
This is the 2 routines `get_string` and `encrypt`:
```cpp
_BYTE *__cdecl encrypt(char *s, int a2, int a3)
{
  size_t v3; // eax
  _BYTE *v5; // [esp+8h] [ebp-10h]
  size_t i; // [esp+Ch] [ebp-Ch]

  debugger_check();
  v3 = strlen(s);
  v5 = calloc(v3, 1u);
  for ( i = 0; strlen(s) > i; ++i )
  {
    if ( s[i] == 32 )
      v5[i] = s[i];
    else
      v5[i] = (a2 * (s[i] - 65) + a3) % 26 + 65;
  }
  return v5;
}

unsigned int __cdecl get_string(int a1)
{
  unsigned int result; // eax
  unsigned int i; // [esp+8h] [ebp-Ch]
  int v3; // [esp+Ch] [ebp-8h]

  debugger_check();
  v3 = 0;
  for ( i = 0; ; ++i )
  {
    result = i;
    if ( i > 0x1F )
      break;
    if ( !(i & 1) )
      *(_BYTE *)(15 - v3++ + a1) = (unsigned int)blah[i];
      // blah = "APRMXCSBCEDISBVXISXWERJRWSZARSQ"
  }
  return result;
}
```
I simply bruteforce the password, using this script
```python
import string
blah = "XAPRMXCSBCEDISBVXISXWERJRWSZARSQ"
table = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
enc_table = {}
def get_string():
	ret = [0] * 16
	c = 0
	for i in range(32):
		if i % 2 == 0:
			ret[15 - c] = blah[i]
			c += 1
	return ''.join(ret)

def enc(c):
	c = ord(c)
	if c == 32:
		return chr(c)
	else:
		c = (17 * (c - 65) + 12) % 26 + 65;
		return chr(c)

for i in table:
	enc_table[enc(i)] = i

r = ''
for i in get_string():
	r += enc_table[i]
print r
```
Run the sciprt above, we got: `IKILLWITHMYHEART`
```
(env) osboxes@osboxes:~/Desktop$ nc challenges.auctf.com 30005
54 68 65 20 6d 61 6e 20 69 6e 20 62 6c 61 63 6b 20 66 6c 65 64 20 61 63 72 6f 73 73 20 74 68 65 20 64 65 73 65 72 74 2c 20 61 6e 64 20 74 68 65 20 67 75 6e 73 6c 69 6e 67 65 72 20 66 6f 6c 6c 6f 77 65 64 2e
Input: IKILLWITHMYHEART
auctf{static_or_dyn@mIc?_12923}
```
The flag is `auctf{static_or_dyn@mIc?_12923}`.