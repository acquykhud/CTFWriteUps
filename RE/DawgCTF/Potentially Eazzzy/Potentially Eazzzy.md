
# Potentially Eazzzy
> xikhud, 13/04/2020.

## Problem
This problem requires us to write a keygen
```python
#!/usr/bin/env python3
# Potentially Eazzzy
# Author: chainsaw10

# If I screwed up and you can't generate a key for your email, I tested this
# program with info@umbccd.io and it should work with that email and an
# appropriate key. Still yell at me in Discord though ;)

try:
    FLAG = open("flag.txt", "r").read()
except:
    FLAG = "DogeCTF{Flag is different on the server}"

import itertools

ALPHABET = [chr(i) for i in range(ord("*"), ord("z")+1)]

def print_flag():
    print("Generating flag...")
    print(FLAG)

a = lambda c: ord(ALPHABET[0]) + (c % len(ALPHABET))

o = lambda c: ord(c)

oa = lambda c: a(o(c))

def indexes(s, needle):
    a = 0
    for idx, c in enumerate(s):
        if c == needle:
            a += idx
    return a

def m(one, two, three, four):
    d = len(ALPHABET)//2
    s = ord(ALPHABET[0])
    s1, s2, s3 = o(one) - s, o(two) - s, o(three) - s
    return (s1 + s2 + s3) % d == four % d

def validate(email, key):
    email = email.strip()
    key = key.strip()

    if len(key) != 32:
        return False

    email = email[:31].ljust(31, "*")
    email += "*"

    for c in itertools.chain(email, key):
        if c not in ALPHABET:
            return False

    if email.count("@") != 1:
        return False

    if key[0] != "Z":
        return False

    dotcount = email.count(".")
    if dotcount < 0 or dotcount >= len(ALPHABET):
        return False

    if a(dotcount) != o(key[1]):
        return False

    if o(key[3]) != a(o(key[1])%30 + o(key[2])%30) + 5:
        return False

    if o(key[2]) != a(indexes(email, "*") + 7):
        return False

    if o(key[4]) != a(sum(o(i) for i in email)%60 + o(key[5])):
        return False

    if o(key[5]) != a(o(key[3]) + 52):
        return False

    if o(key[6]) != a((o(key[7])%8)*2):
        return False

    if o(key[7]) != a(o(key[1]) + o(key[2]) - o(key[3])):
        return False

    if o(key[8]) != a((o(key[6])%16) / 2):
        return False

    if o(key[9]) != a(o(key[6]) + o(key[4]) + o(key[8]) - 4):
        return False

    if o(key[10]) != a((o(key[1])%2) * 8 + o(key[2]) % 3 + o(key[3]) % 4):
        return False

    if not m(email[3], key[11], key[12], 8):
        return False
    if not m(email[7], key[13], key[4], 18):
        return False
    if not m(email[9], key[14], key[3], 23):
        return False
    if not m(email[10], key[15], key[10], 3):
        return False
    if not m(email[11], key[13], key[16], 792):
        return False
    if not m(email[12], key[17], key[4], email.count("d")):
        return False
    if not m(email[13], key[18], key[7], email.count("a")):
        return False
    if not m(email[14], key[19], key[8], email.count("w")):
        return False
    if not m(email[15], key[20], key[1], email.count("g")):
        return False
    if not m(email[16], email[17], key[21], email.count("s")):
        return False
    if not m(email[18], email[19], key[22], email.count("m")):
        return False
    if not m(email[20], key[23], key[17], 9):
        return False
    if not m(email[21], key[24], key[13], 41):
        return False
    if not m(email[22], key[25], key[10], 3):
        return False
    if not m(email[23], key[26], email[14], email.count("1")):
        return False
    if not m(email[24], email[25], key[27], email.count("*")):
        return False
    if not m(email[26], email[27], key[28], 7):
        return False
    if not m(email[28], email[29], key[29], 2):
        return False
    if not m(email[30], key[30], email[18], 4):
        return False
    if not m(email[31], key[31], email[4], 7):
        return False

    return True


def main():
    print("Welcome to Flag Generator 5000")
    print()
    print("Improving the speed quality of CTF solves since 2020")
    print()
    print("You'll need to have your email address and registration key ready.")
    print("Please note the support hotline is closed for COVID-19 and will be")
    print("unavailable until further notice.")
    print()

    email = input("Please enter your email address: ")
    key = input("Please enter your key: ")

    if validate(email, key):
        print_flag()
    else:
        print("License not valid. Please contact support.")

main()

```
## Analyze the code
After reading the code, we can see that the program need two inputs, email and key, but the key nearly depends on the email, so we create a static email, and generate the key.
## Solution
I use this script to generate email and key.
```python
ALPHABET = "*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz"
a = map(ord, ALPHABET)
k = [0x20] * 32
e = "z.z@"[:31].ljust(31, "*") + "*"
e = map(ord, e)



def indexes(s, c):
    a = 0
    for i in range(len(s)):
        if s[i] == c: a += i
    return a

k[0] = ord('Z')
k[1] = a[1]
k[2] = a[0] + ((indexes(e, ord("*")) + 7) % 81)
k[3] = a[(k[1] % 30) + (k[2] % 30)] + 5
k[5] = a[(k[3] + 52) % 81]
k[4] = a[((sum(e) % 60) + k[5]) % 81]
k[7] = a[k[1] % 81] + k[2] - k[3]
k[6] = a[(k[7] % 8) * 2]
k[8] = a[(k[6] % 16) / 2]
k[9] = a[(k[6] + k[4] + k[8] - 4) % 81]
k[10] = a[(k[1] % 2) * 8 + (k[2] % 3) + (k[3] % 4)]

def b(ie,x,ix,y,iy,r):
    for i in a:
        if (x is k and x[ix] != 0x20) or (x is e):
            i = x[ix]
        for j in a:
            if (y is k and y[iy] != 0x20) or (y is e):
                j = y[iy]
            if (e[ie] + i + j - 126) % 40 == r % 40:
                x[ix], y[iy] = i, j
                return

b(3,k,11,k,12,8)
b(7,k,13,k,4,18)
b(9,k,14,k,3,23)

b(10,k,15,k,10,3)
b(11,k,13,k,16,792)
b(12,k,17,k,4,e.count(ord("d")))
b(13,k,18,k,7,e.count(ord("a")))
b(14,k,19,k,8,e.count(ord("w")))
b(15,k,20,k,1,e.count(ord("g")))
b(16,e,17,k,21,e.count(ord("s")))
b(18,e,19,k,22,e.count(ord("m")))

b(20,k,23,k,17,9)
b(21,k,24,k,13,1)
b(22,k,25,k,10,3)
b(23,k,26,e,14,e.count(ord("1")))
b(24,e,25,k,27,e.count(ord("*")))


b(26,e,27,k,28,7)
b(28,e,29,k,29,2)
b(30,k,30,e,18,4)
b(31,k,31,e,4,7)

print ''.join(map(chr, e))
print ''.join(map(chr, k))
```
Run the script, we get:
```
z.z@****************************
Z+5SW`87.A7*D7@H=MENQ**8FH*F1,.1
```
Submit the key, and the flag is `DawgCTF{h0pe_th15_w@snt_t00_eaz^3y_4_u}`.