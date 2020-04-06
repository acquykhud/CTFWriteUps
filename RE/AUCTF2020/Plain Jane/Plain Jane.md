# Plane Jane
> xikhud, 05/04/2020.

## Problem
This is a simple assembly code.

## Static analysis
This is the content:
```assembly
	.file	"plain_asm.c"
	.intel_syntax noprefix
	.text
	.globl	main
	.type	main, @function
main:
.LFB6:
	.cfi_startproc
	push	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.cfi_def_cfa_register 6
	sub	rsp, 16
	mov	eax, 0
	call	func_1
	mov	DWORD PTR -4[rbp], eax
	mov	eax, 0
	call	func_2
	mov	DWORD PTR -8[rbp], eax
	mov	edx, DWORD PTR -8[rbp]
	mov	eax, DWORD PTR -4[rbp]
	mov	esi, edx
	mov	edi, eax
	call	func_3
	mov	DWORD PTR -12[rbp], eax
	mov	eax, 0
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE6:
	.size	main, .-main
	.globl	func_1
	.type	func_1, @function
func_1:
.LFB7:
	.cfi_startproc
	push	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.cfi_def_cfa_register 6
	mov	BYTE PTR -1[rbp], 25
	mov	DWORD PTR -8[rbp], 0
	jmp	.L4
.L5:
	mov	eax, DWORD PTR -8[rbp]
	add	eax, 10
	mov	edx, eax
	mov	eax, edx
	sal	eax, 2
	add	eax, edx
	lea	edx, 0[0+rax*4]
	add	eax, edx
	add	BYTE PTR -1[rbp], al
	add	DWORD PTR -8[rbp], 1
.L4:
	cmp	DWORD PTR -8[rbp], 9
	jle	.L5
	movzx	eax, BYTE PTR -1[rbp]
	mov	DWORD PTR -12[rbp], eax
	mov	eax, DWORD PTR -12[rbp]
	pop	rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE7:
	.size	func_1, .-func_1
	.globl	func_2
	.type	func_2, @function
func_2:
.LFB8:
	.cfi_startproc
	push	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.cfi_def_cfa_register 6
	mov	DWORD PTR -4[rbp], 207
	mov	eax, DWORD PTR -4[rbp]
	pop	rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE8:
	.size	func_2, .-func_2
	.globl	func_3
	.type	func_3, @function
func_3:
.LFB9:
	.cfi_startproc
	push	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.cfi_def_cfa_register 6
	mov	DWORD PTR -36[rbp], edi
	mov	DWORD PTR -40[rbp], esi
	cmp	DWORD PTR -36[rbp], 64
	jg	.L10
	mov	eax, 24
	jmp	.L11
.L10:
	cmp	DWORD PTR -40[rbp], 211
	jle	.L12
	mov	eax, 20
	jmp	.L11
.L12:
	cmp	DWORD PTR -36[rbp], 0
	je	.L13
	cmp	DWORD PTR -40[rbp], 0
	jne	.L13
	mov	eax, 120
	jmp	.L11
.L13:
	cmp	DWORD PTR -36[rbp], 0
	jne	.L14
	cmp	DWORD PTR -40[rbp], 0
	je	.L14
	mov	eax, 220
	jmp	.L11
.L14:
	mov	eax, DWORD PTR -36[rbp]
	or	eax, DWORD PTR -40[rbp]
	mov	DWORD PTR -12[rbp], eax
	mov	eax, DWORD PTR -36[rbp]
	and	eax, DWORD PTR -40[rbp]
	mov	DWORD PTR -16[rbp], eax
	mov	eax, DWORD PTR -36[rbp]
	xor	eax, DWORD PTR -40[rbp]
	mov	DWORD PTR -20[rbp], eax
	mov	DWORD PTR -4[rbp], 0
	mov	DWORD PTR -8[rbp], 0
	jmp	.L15
.L16:
	mov	eax, DWORD PTR -16[rbp]
	sub	eax, DWORD PTR -8[rbp]
	mov	edx, eax
	mov	eax, DWORD PTR -12[rbp]
	add	eax, edx
	add	DWORD PTR -4[rbp], eax
	add	DWORD PTR -8[rbp], 1
.L15:
	mov	eax, DWORD PTR -8[rbp]
	cmp	eax, DWORD PTR -20[rbp]
	jl	.L16
	mov	eax, DWORD PTR -4[rbp]
.L11:
	pop	rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE9:
	.size	func_3, .-func_3
	.ident	"GCC: (Debian 9.2.1-22) 9.2.1 20200104"
	.section	.note.GNU-stack,"",@progbits

```
# Solution
I simply read the code line-by-line, and translate it to equivalent cpp code:
```cpp
#include <stdio.h>
#include <string.h>

typedef unsigned char BYTE;

BYTE f1()
{
	BYTE a = (BYTE)25;
	for (int i = 0; i <= 9; ++i)
	{
		int A = i;
		A += 10;
		int D = A;
		A <<= 2;
		A += D;
		D = A * 4;
		A += D;
		a += (A % 256);
	}
	return a;
}

int f2()
{
	return 207;
}

int f3(int v1, int v2)
{
	if (v2 <= 64)
		return 20;
	if (v1 > 211)
		return 24;
	if (v2 && !v1)
		return 120;
	if (v1 && !v2)
		return 220;
	int tmp;
	int v8 = v2|v1;
	int v7 = v2&v1;
	int v6 = v2^v1;
	int v9 = 0;
	int v10 = 0;
	do 
	{
		tmp = v7 - v9;
		int tmp2 = tmp;
		tmp = v8;
		tmp += tmp2;
		v10 += tmp;
		++v9;
	} while (v9 < v6);
	return v10;
}


int main()
{
	printf("%d\n", f3(f1(), f2()));
	return 0;
}
```
The flag is: `28623`.