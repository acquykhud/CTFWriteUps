# Gym
Another easy problem. Decompile the program using IDA, we got:
```cpp
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int v3; // eax
  int v5; // [rsp+Ch] [rbp-A4h]
  unsigned int i; // [rsp+10h] [rbp-A0h]
  FILE *stream; // [rsp+18h] [rbp-98h]
  char s; // [rsp+20h] [rbp-90h]
  char v9; // [rsp+60h] [rbp-50h]
  unsigned __int64 v10; // [rsp+A8h] [rbp-8h]

  v10 = __readfsqword(0x28u);
  v5 = 211;
  setbuf(stdout, 0LL);
  setbuf(stdin, 0LL);
  setbuf(stderr, 0LL);
  printf("I'm currently %d lbs. Can I be exactly 180? Help me out!", 211LL);
  for ( i = 1; (int)i <= 7; ++i )
  {
    printf("\n-------------------------");
    printf("\nToday is day %d.\n", i);
    printf("\nChoose an activity:");
    printf("\n[1] Eat healthy");
    printf("\n[2] Do 50 push-ups");
    printf("\n[3] Go for a run.");
    printf("\n[4] Sleep 8 hours.");
    puts("\n");
    fgets(&s, 4, stdin);
    v3 = atoi(&s);
    if ( v3 == 2 )
    {
      v5 -= do_pushup(i);
      continue;
    }
    if ( v3 > 2 )
    {
      if ( v3 == 3 )
      {
        v5 -= go_run(i);
LABEL_12:
        v5 -= go_sleep(i);
        continue;
      }
      if ( v3 == 4 )
        goto LABEL_12;
    }
    else if ( v3 == 1 )
    {
      v5 -= eat_healthy(i);
    }
  }
  sleep(3u);
  if ( v5 == 180 )
  {
    stream = fopen("flag.txt", "r");
    if ( !stream )
    {
      puts("Flag File is Missing. Contact a moderator if running on server.");
      exit(0);
    }
    fgets(&v9, 64, stream);
    puts("Congrats on reaching your weight goal!");
    printf("Here is your prize: %s\n", &v9);
  }
  else
  {
    puts("I didn't reach my goal :(");
  }
  return 0;
}
```

We must do some activities in order to have be exactly 180 lbs. Currently, we are 211 lbs (so we need to decrease weight by 31).

 1. `eat_healthy`: decrease weight by 4.
 2. `go_run`: decrease weight by 2.
 3. `go_sleep`: decrease weight by 3.
 4. `do_pushup`: decrease weight by 1.

We are limited to only do 7 activities, the maximum weight we can decrease is `28`, but there is a trick here, when you input `3`, we will do both `go_run` and `go_sleep`.

## Solution
Send `3` six times and `2` one time to the server, we get the flag
`tjctf{w3iGht_l055_i5_d1ff1CuLt}`.