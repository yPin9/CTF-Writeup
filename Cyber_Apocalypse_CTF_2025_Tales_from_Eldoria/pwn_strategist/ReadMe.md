# strategist

> Heap chunk's size overwrite

## Decompile

```C
int __fastcall __noreturn main(int argc, const char **argv, const char **envp)
{
  unsigned __int64 v3; // rax
  char s[808]; // [rsp+0h] [rbp-330h] BYREF
  unsigned __int64 v5; // [rsp+328h] [rbp-8h]

  v5 = __readfsqword(0x28u);
  memset(s, 0, 0x320uLL);
  banner();
  while ( 1 )
  {
    while ( 1 )
    {
      while ( 1 )
      {
        v3 = menu();
        if ( v3 != 2 )
          break;
        show_plan(s);
      }
      if ( v3 > 2 )
        break;
      if ( v3 != 1 )
        goto LABEL_13;
      create_plan(s);
    }
    if ( v3 == 3 )
    {
      edit_plan(s);
    }
    else
    {
      if ( v3 != 4 )
      {
LABEL_13:
        printf("%s\n[%sSir Alaric%s]: This plan will lead us to defeat!\n\n", "\x1B[1;31m", "\x1B[1;33m", "\x1B[1;31m");
        exit(1312);
      }
      delete_plan(s);
    }
  }
}
```

```C
unsigned __int64 __fastcall delete_plan(__int64 a1)
{
  unsigned int v2; // [rsp+14h] [rbp-Ch] BYREF
  unsigned __int64 v3; // [rsp+18h] [rbp-8h]

  v3 = __readfsqword(0x28u);
  printf("%s\n[%sSir Alaric%s]: Which plan you want to delete?\n\n> ", "\x1B[1;34m", "\x1B[1;33m", "\x1B[1;34m");
  v2 = 0;
  __isoc99_scanf("%d", &v2);
  if ( v2 > 0x63 || !*(_QWORD *)(8LL * (int)v2 + a1) )
  {
    printf("%s\n[%sSir Alaric%s]: There is no such plan!\n\n", "\x1B[1;31m", "\x1B[1;33m", "\x1B[1;31m");
    exit(1312);
  }
  free(*(void **)(8LL * (int)v2 + a1));
  *(_QWORD *)(8LL * (int)v2 + a1) = 0LL;
  printf("%s\n[%sSir Alaric%s]: We will remove this plan!\n\n", "\x1B[1;32m", "\x1B[1;33m", "\x1B[1;32m");
  return __readfsqword(0x28u) ^ v3;
}
```

```C
unsigned __int64 __fastcall delete_plan(void **ptr)
{
  unsigned int index; // [rsp+14h] [rbp-Ch] BYREF
  unsigned __int64 v3; // [rsp+18h] [rbp-8h]

  v3 = __readfsqword(0x28u);
  printf("%s\n[%sSir Alaric%s]: Which plan you want to delete?\n\n> ", "\x1B[1;34m", "\x1B[1;33m", "\x1B[1;34m");
  index = 0;
  __isoc99_scanf("%d", &index);
  if ( index > 0x63 || !ptr[index] )
  {
    printf("%s\n[%sSir Alaric%s]: There is no such plan!\n\n", "\x1B[1;31m", "\x1B[1;33m", "\x1B[1;31m");
    exit(1312);
  }
  free(ptr[index]);
  ptr[index] = 0LL;
  printf("%s\n[%sSir Alaric%s]: We will remove this plan!\n\n", "\x1B[1;32m", "\x1B[1;33m", "\x1B[1;32m");
  return __readfsqword(0x28u) ^ v3;
}
```




本來以為會是什麼 UAF 的問題，但看到他這邊有乖乖清掉



## key idea

```C
unsigned __int64 __fastcall edit_plan(__int64 a1)
{
  size_t v1; // rax
  unsigned int v3; // [rsp+14h] [rbp-Ch] BYREF
  unsigned __int64 v4; // [rsp+18h] [rbp-8h]

  v4 = __readfsqword(0x28u);
  printf("%s\n[%sSir Alaric%s]: Which plan you want to change?\n\n> ", "\x1B[1;34m", "\x1B[1;33m", "\x1B[1;34m");
  v3 = 0;
  __isoc99_scanf("%d", &v3);
  if ( v3 > 0x63 || !*(_QWORD *)(8LL * (int)v3 + a1) )
  {
    printf("%s\n[%sSir Alaric%s]: There is no such plan!\n\n", "\x1B[1;31m", "\x1B[1;33m", "\x1B[1;31m");
    exit(1312);
  }
  printf("%s\n[%sSir Alaric%s]: Please elaborate on your new plan.\n\n> ", "\x1B[1;34m", "\x1B[1;33m", "\x1B[1;34m");
  v1 = strlen(*(const char **)(8LL * (int)v3 + a1));
  read(0, *(void **)(8LL * (int)v3 + a1), v1);
  putchar(10);
  return __readfsqword(0x28u) ^ v4;
}
```
```c
unsigned __int64 __fastcall edit_plan(void **ptr)
{
  size_t length; // rax
  unsigned int index; // [rsp+14h] [rbp-Ch] BYREF
  unsigned __int64 v4; // [rsp+18h] [rbp-8h]

  v4 = __readfsqword(0x28u);
  printf("%s\n[%sSir Alaric%s]: Which plan you want to change?\n\n> ", "\x1B[1;34m", "\x1B[1;33m", "\x1B[1;34m");
  index = 0;
  __isoc99_scanf("%d", &index);
  if ( index > 99 || !ptr[index] )
  {
    printf("%s\n[%sSir Alaric%s]: There is no such plan!\n\n", "\x1B[1;31m", "\x1B[1;33m", "\x1B[1;31m");
    exit(1312);
  }
  printf("%s\n[%sSir Alaric%s]: Please elaborate on your new plan.\n\n> ", "\x1B[1;34m", "\x1B[1;33m", "\x1B[1;34m");
  length = strlen((const char *)ptr[index]);
  read(0, ptr[index], length);
  putchar(10);
  return __readfsqword(0x28u) ^ v4;
}
```



這邊修改是直接去讀 data 的長度，但我們知道一塊 chunk 最後的資料會放在下一塊 chunk 的首八個 bytes，剛好這8bytes會緊鄰下一塊 chunk header 紀錄 chunk size 的地方，所以他這邊回傳的 length 會包含這個 chunk size()，`strlen()` 的回傳值就會是原本的大小加上 4bytes，而這多的 4bytes 就可以 overflow，後面的 trick 就很一般，`free_hook` 覆寫 `call free()`

> 值得一提的是，這是我第一次排 heap ，挺有成就感的

```

+------------------------------+
|            8bytes            |
+---------------+--------------+
| pre data/size |     size     | 
--------------------------------
|                              |
|             data             |
|                              |
+--------------+---------------+
 pre data/size |     size      |
       ^
       |______ padding here 我們 strlen 的回傳值就會是 chunk size + 4 bytes(這就是右邊那邊的 size 的地方)_
 

```

對了 要知道 libc address 就用 unsortbin 那招就可以了 

把 chunk 送進 unsortbin，然後要出來，這時候這塊 chunk 的頭就是 `&main_arena` 然後 `show()`，拿到 `&main_arena`，扣掉 offset，就是 libc base address 了，這個 offset 直接 gdb 裡面用 vmmap 看就可以了