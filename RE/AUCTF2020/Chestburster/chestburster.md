# Chestburster
> xikhud, 05/04/2020.

## Problem
This is a simple challenge.

## Static analysis
The program asks us to input a password, then check the password, if it's true, we get the flag.
```cpp
BOOL check()
{
  FILE *v0; // eax
  int v1; // ecx
  signed int pwLen; // kr00_4
  const char *enc_pw; // edi
  unsigned int v4; // eax
  signed int v5; // edx
  char v6; // cl
  signed int v7; // edx
  int v8; // ecx
  char v9; // bl
  int v10; // edi
  int v11; // ecx
  signed int v12; // edx
  int i; // ebx
  int v14; // ecx
  unsigned int v15; // kr04_4
  int v16; // edx
  int v17; // ecx
  int v18; // esi
  int v19; // edi
  char *v20; // edx
  char v21; // cl
  int v22; // edx
  int v23; // ecx
  int v24; // ecx
  int v26; // [esp+0h] [ebp-214h]
  const char *_enc_pw; // [esp+4h] [ebp-210h]
  int v28; // [esp+8h] [ebp-20Ch]
  signed int v29; // [esp+8h] [ebp-20Ch]
  int v30; // [esp+Ch] [ebp-208h]
  char password[512]; // [esp+10h] [ebp-204h]

  mb_printf("\tYou know the drill, give me some input and I'll tell you if it's right\n");
  mb_printf("\n\t");
  v0 = (FILE *)_acrt_iob_func(0);
  fgets(password, 512, v0);
  v1 = &password[strlen(password) + 1] - &password[1];
  if ( *((_BYTE *)&v30 + v1 + 3) == '\n' )
  {
    *((_BYTE *)&v30 + v1 + 3) = 0;            
  }
  pwLen = strlen(password);
  enc_pw = (const char *)calloc((pwLen + 1) | -__CFADD__(pwLen, 1), 1u);
  _enc_pw = enc_pw;
  if ( !enc_pw )
  {
    mb_printf("Error: out of memory\n");
    exit(1);
  }
  v4 = 0;
  v5 = 0;
  if ( pwLen <= 0 )
  {
    v4 = 0;
  }
  else
  {
    do
    {
      if ( v5 )
      {
        v6 = password[v4++];
        enc_pw[v5] = v6; // <--------------------- bp here
      }
      v5 += v4 + 2;                        
    }
    while ( v5 < pwLen );
    v7 = 0;
    v8 = 0;
    v30 = 0;
    v28 = 0;
    do
    {
      v9 = password[v4++];
      if ( !v30 )
      {
        v7 = 1;
      }
      v10 = v28;
      v11 = v8 + 1;
      if ( v30 )
      {
        v10 = v11;
      }
      v28 = v10;
      enc_pw = _enc_pw;
      _enc_pw[v30] = v9;  // <--------------------- bp here              
      v8 = v28;
      v7 += v28 + 2;
      v30 = v7;
    }
    while ( v7 < pwLen );
    v12 = 1;
    for ( i = 0; v12 < pwLen; v12 += v14 + 3 )
    {
      v14 = i + 1;
      if ( v12 < 7 )
      {
        v14 = i;
      }
      i = v14;
      _enc_pw[v12] = password[v4++];  // <--------------------- bp here
    }
  }
  v15 = strlen(password);
  v16 = 3;
  v30 = 3;
  if ( v4 < v15 )
  {
    v29 = 3;
    v17 = (int)&enc_pw[v15 - 3];
    do
    {
      v18 = v16;
      v19 = v16;
      v20 = (char *)(v17 - 3);
      if ( v30 )
      {
        v20 = (char *)v17;
      }
      v21 = password[v4++];
      *v20 = v21;  // <--------------------- bp here
      v26 = (int)(v20 - 1);
      v22 = v29 - 1;
      if ( v18 )
      {
        v22 = v18;
      }
      v23 = v29 - 1;
      v16 = v22 - 1;
      v30 = v16;
      if ( v19 )
      {
        v23 = v29;
      }
      v29 = v23;
      v17 = v26;
    }
    while ( v4 < v15 );
    enc_pw = _enc_pw;
  }
  v24 = strcmp(enc_pw, "welcome_to_the_jungle!");
  if ( v24 )
  {
    v24 = -(v24 < 0) | 1;
  }
  return v24 == 0;
}
```
# Solution
We can see that, the program permutes our password in some way.
I was too lazy to read the code, so I put breakpoint at the place where `enc_pw[idx]` is assigned, and check the index.
There are total of 4 breakpoints, you can see where they are in the code above.
```python
o1 = (2, 5, 9, 14, 20, 27)
o2 = (0, 3, 6, 10, 15, 21, 28, 97)
o3 = (1, 4, 7, 11, 16, 22)
o4 = (19, 18, 17, 13, 12, 8)

win = 'welcome_to_the_jungle!'
r = ''
for i in o1:
    if i < len(win):
        r += win[i]
for i in o2:
    if i < len(win):
        r += win[i]
for i in o3:
    if i < len(win):
        r += win[i]
for i in o4:
    if i < len(win):
        r += win[i]

print r
```
Run the script, we get: `lmo_ewce_j!eo_tulgneht`