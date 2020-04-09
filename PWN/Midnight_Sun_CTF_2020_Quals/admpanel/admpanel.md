# amdpanel
> LongChampion, 06/04/2020

## Challenge
This challenge have simple inteface:
```
LOG: [OPERATION: CONNECT] Todo: log IP address for traceability!
---=-=-=-=-=-=-=-=-=---
-      Admin panel    -
-
- [0] - Help
- [1] - Authenticate
- [2] - Execute command
- [3] - Exit
---=-=-=-=-=-=-=-=-=---
 > 
```
After reversing, I see that we can login with account `admin:password` and execute any command start with `id`. Yes, it is command injection.

## Solution
You can solve this challenge by hand: login with account `admin:password`, then execute `id;/bin/sh;` to get the shell.
