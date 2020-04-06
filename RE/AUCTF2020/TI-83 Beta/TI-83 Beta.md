# TI-83 Beta
> xikhud, 05/04/2020.

## Problem
This is a simple challenge, but it has a simple technique make decompiler produce wrong result !

## Static analysis
There is nothing suspicious in the binary, all functions are fine.
But when I take a closer look, I find this:
```assembly
.text:00412560                 push    ebp
.text:00412561                 mov     ebp, esp
.text:00412563                 sub     esp, 0C0h
.text:00412569                 push    ebx
.text:0041256A                 push    esi
.text:0041256B                 push    edi
.text:0041256C                 lea     edi, [ebp-0C0h]
.text:00412572                 mov     ecx, 30h ; '0'
.text:00412577                 mov     eax, 0CCCCCCCCh
.text:0041257C                 rep stosd
.text:0041257E                 xor     eax, eax
.text:00412580                 jz      short near ptr loc_412582+2
.text:00412582
.text:00412582 loc_412582:                             ; CODE XREF: .text:00412580↑j
.text:00412582                 jmp     far ptr 0:0B858h
.text:00412582 ; ---------------------------------------------------------------------------
.text:00412589                 db 83h, 0ECh, 20h
.text:0041258C                 dd 612404C6h, 12444C6h, 2444C675h, 44C66302h, 0C6740324h
.text:0041258C                 dd 66042444h, 52444C6h, 2444C67Bh, 0C0336F06h, 58EA0274h
.text:0041258C                 dd 72444C6h, 2444C66Fh, 44C67008h, 0C6730924h, 5F0A2444h
.text:0041258C                 dd 0B2444C6h, 2444C664h, 44C6690Ch, 0C6640D24h, 5F0E2444h
.text:0041258C                 dd 0F2444C6h, 2444C669h, 44C65F10h, 0C6641124h, 6F122444h
.text:0041258C                 dd 132444C6h, 2444C65Fh, 44C67414h, 0C6681524h, 74162444h
.text:0041258C                 dd 172444C6h, 2444C67Dh, 44C60A18h, 54001924h, 0FFEA37E8h
.text:0041258C                 dd 24648BFFh, 0A16408h, 8B000000h, 64008B00h, 0A3h, 8C48300h
.text:0041258C                 dd 815B5E5Fh, 0C0C4h, 0E8EC3B00h, 0FFFFEC31h, 0C35DE58Bh
.text:0041258C                 dd 0Fh dup(0CCCCCCCCh)
```
The first two instructions are `push ebp, mov ebp, esp`, which look like the prototype of a function in assembly, but IDA doesn't regconize it. Let's fix this.
Select address 0x412582 to 0x41258C with the cursor, then press 'U' `(undefine)`, then put the cursor at address 0x412584, press 'C' `(code)`, and we have:
```assembly
.text:00412560                 push    ebp
.text:00412561                 mov     ebp, esp
.text:00412563                 sub     esp, 0C0h
.text:00412569                 push    ebx
.text:0041256A                 push    esi
.text:0041256B                 push    edi
.text:0041256C                 lea     edi, [ebp-0C0h]
.text:00412572                 mov     ecx, 30h ; '0'
.text:00412577                 mov     eax, 0CCCCCCCCh
.text:0041257C                 rep stosd
.text:0041257E                 xor     eax, eax
.text:00412580                 jz      short loc_412584
.text:00412580 ; ---------------------------------------------------------------------------
.text:00412582                 db 0EAh ; ê
.text:00412583                 db  58h ; X
.text:00412584 ; ---------------------------------------------------------------------------
.text:00412584
.text:00412584 loc_412584:                             ; CODE XREF: .text:00412580↑j
.text:00412584                 mov     eax, 0
.text:00412589                 sub     esp, 20h
.text:0041258C                 mov     byte ptr [esp], 61h ; 'a'
.text:00412590                 mov     byte ptr [esp+1], 75h ; 'u'
.text:00412595                 mov     byte ptr [esp+2], 63h ; 'c'
.text:0041259A                 mov     byte ptr [esp+3], 74h ; 't'
.text:0041259F                 mov     byte ptr [esp+4], 66h ; 'f'
.text:004125A4                 mov     byte ptr [esp+5], 7Bh ; '{'
.text:004125A9                 mov     byte ptr [esp+6], 6Fh ; 'o'
.text:004125AE                 xor     eax, eax
.text:004125B0                 jz      short near ptr loc_4125B2+2
.text:004125B2
.text:004125B2 loc_4125B2:                             ; CODE XREF: .text:004125B0↑j
.text:004125B2                 jmp     far ptr 6F07h:2444C658h
.text:004125B2 ; ---------------------------------------------------------------------------
.text:004125B9                 db 0C6h ; Æ
.text:004125BA                 db  44h ; D
.text:004125BB                 db  24h ; $
.text:004125BC                 db    8
.text:004125BD                 db  70h ; p
```
Do you see `a,u,c,t,f` ?
We do it one more time (at address 0x4125B4):
```assembly
text:00412589                 sub     esp, 20h
.text:0041258C                 mov     byte ptr [esp], 61h ; 'a'
.text:00412590                 mov     byte ptr [esp+1], 75h ; 'u'
.text:00412595                 mov     byte ptr [esp+2], 63h ; 'c'
.text:0041259A                 mov     byte ptr [esp+3], 74h ; 't'
.text:0041259F                 mov     byte ptr [esp+4], 66h ; 'f'
.text:004125A4                 mov     byte ptr [esp+5], 7Bh ; '{'
.text:004125A9                 mov     byte ptr [esp+6], 6Fh ; 'o'
.text:004125AE                 xor     eax, eax
.text:004125B0                 jz      short loc_4125B4
.text:004125B0 ; ---------------------------------------------------------------------------
.text:004125B2                 db 0EAh ; ê
.text:004125B3                 db  58h ; X
.text:004125B4 ; ---------------------------------------------------------------------------
.text:004125B4
.text:004125B4 loc_4125B4:                             ; CODE XREF: .text:004125B0↑j
.text:004125B4                 mov     byte ptr [esp+7], 6Fh ; 'o'
.text:004125B9                 mov     byte ptr [esp+8], 70h ; 'p'
.text:004125BE                 mov     byte ptr [esp+9], 73h ; 's'
.text:004125C3                 mov     byte ptr [esp+0Ah], 5Fh ; '_'
.text:004125C8                 mov     byte ptr [esp+0Bh], 64h ; 'd'
.text:004125CD                 mov     byte ptr [esp+0Ch], 69h ; 'i'
.text:004125D2                 mov     byte ptr [esp+0Dh], 64h ; 'd'
.text:004125D7                 mov     byte ptr [esp+0Eh], 5Fh ; '_'
.text:004125DC                 mov     byte ptr [esp+0Fh], 69h ; 'i'
.text:004125E1                 mov     byte ptr [esp+10h], 5Fh ; '_'
.text:004125E6                 mov     byte ptr [esp+11h], 64h ; 'd'
.text:004125EB                 mov     byte ptr [esp+12h], 6Fh ; 'o'
.text:004125F0                 mov     byte ptr [esp+13h], 5Fh ; '_'
.text:004125F5                 mov     byte ptr [esp+14h], 74h ; 't'
.text:004125FA                 mov     byte ptr [esp+15h], 68h ; 'h'
.text:004125FF                 mov     byte ptr [esp+16h], 74h ; 't'
.text:00412604                 mov     byte ptr [esp+17h], 7Dh ; '}'
.text:00412609                 mov     byte ptr [esp+18h], 0Ah
.text:0041260E                 mov     byte ptr [esp+19h], 0
...
```
# Solution
Do you see the flag ^^ ?
`auctf{oops_did_i_do_tht}`