# laconic

> SROP

## Decompile

```C
public _start
_start proc near
mov     rdi, 0          ; Alternative name is '_start'
                        ; __start
mov     rsi, rsp
sub     rsi, 8
mov     rdx, 106h
syscall                 ; LINUX -
retn
_start endp
```


## Key idea

* 經典題，就那樣
* 放好 fake stack 踩 `mov rax,0xf;syscall`
* `bin/sh` 藏在整份 binary 的尾巴
