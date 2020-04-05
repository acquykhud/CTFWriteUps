
# Easy As Pie!
> xikhud, 05/04/2020.

## Problem
With this problem, the author did not provide the executable file, so we have to do it on the server. The challenge provides a custom shell, which has 4 simple commands.

 - ls: list files.
 - write \<content\> \<filename\>: write content to the beginning of filename.
 - help: show helps.
 - cat \<filename\>: display contents in filename.

## Solution
First, we list all the file in the current directory using `ls`
```bash
user@pyshell$ ls
acl.txt
user.txt
flag.txt
```
We see the file `flag.txt`, which might be the flag we are searching for, but:
```bash
user@pyshell$ cat flag.txt
Don't have da permzzz
```
We don't have the permission to read `flag.txt`. So we tried another files:
```bash
user@pyshell$ cat user.txt
this is some user content. I bet u wish the flag was here
user@pyshell$ cat acl.txt
user.txt:user:600
.acl.txt:root:600
.flag.txt:user:600
flag.txt:root:600
acl.txt:root:606
```
Yes, we can read `acl.txt` and `user.txt`. The file `acl.txt` contains information about permission of the files in the directory.
Remember `write` command ? Yes, we use it to write the fake permission to `acl.txt`, then use `cat` to read the flag.
```bash
user@pyshell$ write flag.txt:user:600 acl.txt
flag.txt:user:600
user@pyshell$ cat flag.txt
aUctf_{h3y_th3_fl4g}
```
But this is the fake flag, it doesn't start with '`auctf`', so we tried to read all the files:
```bash
user@pyshell$ write .acl.txt:user:600 acl.txt
.acl.txt:user:600
user@pyshell$ cat .acl.txt
auctf{h4_y0u_g0t_tr0ll3d_welC0m#_t0_pWN_l@nd}
user@pyshell$
```
And the real flag: `auctf{h4_y0u_g0t_tr0ll3d_welC0m#_t0_pWN_l@nd}`