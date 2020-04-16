
# Nash!
> xikhud, 13/04/2020.

## Problem
`Welcome to Nash! It's a NoSpaceBash! All you have to do is display the flag. It's right there.
Oh yeah...you can't use any spaces... Good luck!`

 - This is a custom bash problem, we must not use any space character.

## Solution
```
(env) osboxes@osboxes:~/Desktop$ nc ctf.umbccd.io 4600
nash> ls
flag.txt  nash
nash> cat flag.txt
/bin/bash: line 1: catflag.txt: command not found
nash> cat<flag.txt
DawgCTF{L1k3_H0W_gr3a+_R_sp@c3s_Th0uGh_0mg}
nash>
```
And the flag is `DawgCTF{L1k3_H0W_gr3a+_R_sp@c3s_Th0uGh_0mg}`