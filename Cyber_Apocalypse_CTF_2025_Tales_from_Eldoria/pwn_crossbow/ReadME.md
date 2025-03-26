# crossbow

> ROP

## Decompile

```C
int __fastcall main(int argc, const char **argv, const char **envp)
{
  setvbuf(&_stdin_FILE, 0LL, 2LL, 0LL);
  setvbuf(&_stdout_FILE, 0LL, 2LL, 0LL);
  alarm(4882LL);
  banner();
  training();
  return 0;
}
```

```C
__int64 __fastcall training(__int64 a1, __int64 a2, __int64 a3, __int64 a4, int a5, int a6)
{
  int v6; // r8d
  int v7; // r9d
  char v9[32]; // [rsp+0h] [rbp-20h] BYREF

  printf(
    (unsigned int)"%s\n[%sSir Alaric%s]: You only have 1 shot, don't miss!!\n",
    (unsigned int)"\x1B[1;34m",
    (unsigned int)"\x1B[1;33m",
    (unsigned int)"\x1B[1;34m",
    a5,
    a6,
    v9[0]);
  target_dummy(v9);
  return printf(
           (unsigned int)"%s\n[%sSir Alaric%s]: That was quite a shot!!\n\n",
           (unsigned int)"\x1B[1;34m",
           (unsigned int)"\x1B[1;33m",
           (unsigned int)"\x1B[1;34m",
           v6,
           v7,
           v9[0]);
}
```

```C
__int64 __fastcall target_dummy(__int64 a1, __int64 a2, __int64 a3, __int64 a4, int a5, int a6)
{
  int v6; // edx
  int v7; // ecx
  int v8; // r8d
  int v9; // r9d
  int v10; // r8d
  int v11; // r9d
  _QWORD *v12; // rbx
  int v13; // r8d
  int v14; // r9d
  __int64 result; // rax
  int v16; // r8d
  int v17; // r9d
  int v18; // [rsp+1Ch] [rbp-14h] BYREF

  printf(
    (unsigned int)"%s\n[%sSir Alaric%s]: Select target to shoot: ",
    (unsigned int)"\x1B[1;34m",
    (unsigned int)"\x1B[1;33m",
    (unsigned int)"\x1B[1;34m",
    a5,
    a6);
  if ( (unsigned int)scanf((unsigned int)"%d%*c", (unsigned int)&v18, v6, v7, v8, v9) != 1 )
  {
    printf(
      (unsigned int)"%s\n[%sSir Alaric%s]: Are you aiming for the birds or the target kid?!\n\n",
      (unsigned int)"\x1B[1;31m",
      (unsigned int)"\x1B[1;33m",
      (unsigned int)"\x1B[1;31m",
      v10,
      v11);
    exit(1312LL);
  }
  v12 = (_QWORD *)(8LL * v18 + a1);
  *v12 = calloc(1LL, 128LL);
  if ( !*v12 )
  {
    printf(
      (unsigned int)"%s\n[%sSir Alaric%s]: We do not want cowards here!!\n\n",
      (unsigned int)"\x1B[1;31m",
      (unsigned int)"\x1B[1;33m",
      (unsigned int)"\x1B[1;31m",
      v13,
      v14);
    exit(6969LL);
  }
  printf(
    (unsigned int)"%s\n[%sSir Alaric%s]: Give me your best warcry!!\n\n> ",
    (unsigned int)"\x1B[1;34m",
    (unsigned int)"\x1B[1;33m",
    (unsigned int)"\x1B[1;34m",
    v13,
    v14);
  result = fgets_unlocked(*(_QWORD *)(8LL * v18 + a1), 128LL, &_stdin_FILE);
  if ( !result )
  {
    printf(
      (unsigned int)"%s\n[%sSir Alaric%s]: Is this the best you have?!\n\n",
      (unsigned int)"\x1B[1;31m",
      (unsigned int)"\x1B[1;33m",
      (unsigned int)"\x1B[1;31m",
      v16,
      v17);
    exit(69LL);
  }
  return result;
}
```

## Key idea

```C
  v12 = (_QWORD *)(8LL * v18 + a1);
  *v12 = calloc(1LL, 128LL);
```

把 `v12` 控到 `old rbp`，然後在這個空間塞 ROP (return 的時候會 `leave;ret;`，會讓 rsp 設過去這邊開好的空間)，就是 stack pivot，只是要知道要 pivot 到哪裡，這邊也是一步步 gdb 去 trace 的

> `leave == pop rbp;mov rsp,rbp`

```C
  result = fgets_unlocked(*(_QWORD *)(8LL * v18 + a1), 128LL, &_stdin_FILE);

```

這邊塞 ROP，沒啥問題